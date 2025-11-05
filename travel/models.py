from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

from businesses.models import Business, City, Country, Category

User = get_user_model()


class Tag(models.Model):
    """Content tags for organizing articles"""
    
    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    color = models.CharField(_('color'), max_length=7, default='#007cba', help_text='Hex color code')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArticleCategory(models.Model):
    """Categories for travel articles"""
    
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True, help_text='Emoji or FontAwesome icon')
    color = models.CharField(_('color'), max_length=7, default='#28a745', help_text='Hex color code')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    is_active = models.BooleanField(_('is active'), default=True)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Article Category')
        verbose_name_plural = _('Article Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Travel articles and city guides"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('review', _('Under Review')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    
    ARTICLE_TYPES = [
        ('guide', _('City Guide')),
        ('itinerary', _('Travel Itinerary')),
        ('review', _('Travel Review')),
        ('tips', _('Travel Tips')),
        ('culture', _('Local Culture')),
        ('business_feature', _('Business Feature')),
        ('seasonal', _('Seasonal Content')),
        ('comparison', _('City/Business Comparison')),
    ]
    
    # Basic Information
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    subtitle = models.CharField(_('subtitle'), max_length=300, blank=True)
    excerpt = models.TextField(_('excerpt'), max_length=500, help_text='Short description for listings')
    
    # Content
    content = models.TextField(_('content'), help_text='Main article content (supports Markdown)')
    featured_image = models.ImageField(_('featured image'), upload_to='articles/', blank=True)
    featured_image_alt = models.CharField(_('featured image alt text'), max_length=200, blank=True)
    
    # Classification
    article_type = models.CharField(_('article type'), max_length=20, choices=ARTICLE_TYPES, default='guide')
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('category')
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))
    
    # Location Association
    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_('countries'),
        help_text='Countries this article covers'
    )
    cities = models.ManyToManyField(
        City,
        blank=True,
        verbose_name=_('cities'),
        help_text='Cities this article covers'
    )
    featured_businesses = models.ManyToManyField(
        Business,
        through='ArticleBusinessFeature',
        blank=True,
        verbose_name=_('featured businesses')
    )
    
    # Publishing
    status = models.CharField(_('status'), max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='travel_articles',
        verbose_name=_('author')
    )
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    
    # SEO
    meta_title = models.CharField(_('meta title'), max_length=60, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=160, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    featured = models.BooleanField(_('featured'), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['article_type', 'featured']),
            models.Index(fields=['view_count']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != 'published':
            self.published_at = None
            
        # Auto-generate meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('travel:article_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at
    
    @property
    def reading_time(self):
        """Estimate reading time based on content length"""
        words = len(self.content.split())
        return max(1, round(words / 200))  # Assuming 200 words per minute
    
    def increment_view_count(self):
        """Increment view count efficiently"""
        Article.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)


class ArticleBusinessFeature(models.Model):
    """Through model for articles featuring businesses"""
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    description = models.TextField(_('description'), blank=True, help_text='Why this business is featured')
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Article Business Feature')
        verbose_name_plural = _('Article Business Features')
        ordering = ['sort_order', 'created_at']
        unique_together = ['article', 'business']
    
    def __str__(self):
        return f"{self.article.title} - {self.business.name}"


class TravelItinerary(models.Model):
    """Structured travel itineraries with day-by-day planning"""
    
    DURATION_CHOICES = [
        ('half_day', _('Half Day (4 hours)')),
        ('full_day', _('Full Day (8 hours)')),
        ('weekend', _('Weekend (2 days)')),
        ('3_days', _('3 Days')),
        ('week', _('1 Week')),
        ('custom', _('Custom Duration')),
    ]
    
    # Basic Information
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'))
    
    # Location
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('city'))
    
    # Duration
    duration_type = models.CharField(_('duration type'), max_length=15, choices=DURATION_CHOICES, default='full_day')
    custom_duration_days = models.PositiveIntegerField(_('custom duration (days)'), null=True, blank=True)
    
    # Content
    featured_image = models.ImageField(_('featured image'), upload_to='itineraries/', blank=True)
    total_cost_estimate = models.DecimalField(
        _('total cost estimate'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Estimated cost in EUR'
    )
    
    # Publishing
    is_published = models.BooleanField(_('is published'), default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    
    # Analytics
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    featured = models.BooleanField(_('featured'), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Travel Itinerary')
        verbose_name_plural = _('Travel Itineraries')
        ordering = ['-featured', '-view_count', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.city.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.city.name}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('travel:itinerary_detail', kwargs={'slug': self.slug})
    
    @property
    def duration_display(self):
        if self.duration_type == 'custom' and self.custom_duration_days:
            return f"{self.custom_duration_days} days"
        return dict(self.DURATION_CHOICES)[self.duration_type]


class ItineraryDay(models.Model):
    """Individual days within an itinerary"""
    
    itinerary = models.ForeignKey(
        TravelItinerary,
        on_delete=models.CASCADE,
        related_name='days',
        verbose_name=_('itinerary')
    )
    day_number = models.PositiveIntegerField(_('day number'))
    title = models.CharField(_('title'), max_length=200, blank=True)
    description = models.TextField(_('description'), blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Itinerary Day')
        verbose_name_plural = _('Itinerary Days')
        ordering = ['day_number']
        unique_together = ['itinerary', 'day_number']
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title or 'Untitled'}"


class ItineraryStop(models.Model):
    """Individual stops/activities within an itinerary day"""
    
    TIME_SLOTS = [
        ('morning', _('Morning (9:00-12:00)')),
        ('afternoon', _('Afternoon (12:00-18:00)')),
        ('evening', _('Evening (18:00-22:00)')),
        ('night', _('Night (22:00+)')),
        ('custom', _('Custom Time')),
    ]
    
    day = models.ForeignKey(
        ItineraryDay,
        on_delete=models.CASCADE,
        related_name='stops',
        verbose_name=_('day')
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('business')
    )
    
    # Activity Details
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    time_slot = models.CharField(_('time slot'), max_length=15, choices=TIME_SLOTS, default='morning')
    custom_time = models.TimeField(_('custom time'), null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(_('duration (minutes)'), default=60)
    
    # Costs
    estimated_cost = models.DecimalField(
        _('estimated cost'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Cost in EUR'
    )
    
    # Ordering
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    # Tips
    tips = models.TextField(_('tips'), blank=True, help_text='Helpful tips for this stop')
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Itinerary Stop')
        verbose_name_plural = _('Itinerary Stops')
        ordering = ['sort_order', 'custom_time']
    
    def __str__(self):
        return f"{self.day.itinerary.title} - Day {self.day.day_number}: {self.title}"


class ArticleView(models.Model):
    """Track article views for analytics"""
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Article View')
        verbose_name_plural = _('Article Views')
        indexes = [
            models.Index(fields=['article', 'viewed_at']),
            models.Index(fields=['ip_address', 'viewed_at']),
        ]


class ArticleImage(models.Model):
    """Images associated with travel articles"""
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('article')
    )
    image = models.ImageField(
        _('image'),
        upload_to='travel_images/%Y/%m/%d/',
        help_text='Generated or uploaded image for the article'
    )
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    alt_text = models.CharField(_('alt text'), max_length=200, blank=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    order = models.PositiveIntegerField(_('order'), default=0)
    
    # AI generation metadata
    generated_by_ai = models.BooleanField(_('generated by AI'), default=True)
    generation_prompt = models.TextField(_('generation prompt'), blank=True)
    generation_style = models.CharField(_('generation style'), max_length=50, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Article Image')
        verbose_name_plural = _('Article Images')
        ordering = ['order', '-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['article', 'is_featured']),
            models.Index(fields=['article', 'order']),
        ]
    
    def __str__(self):
        return f"{self.article.title} - Image {self.id}"