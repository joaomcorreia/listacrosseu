from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()


class Category(models.Model):
    """Business categories"""
    
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True)  # Emoji or icon class
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
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def is_parent(self):
        return self.parent is None
    
    def get_full_path(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Country(models.Model):
    """EU Countries"""
    
    name = models.CharField(_('name'), max_length=100, unique=True)
    code = models.CharField(_('code'), max_length=2, unique=True)  # ISO country code
    slug = models.SlugField(_('slug'), unique=True, blank=True)  # SEO-friendly URL slug
    flag_image = models.ImageField(upload_to='flags/', blank=True)
    is_eu_member = models.BooleanField(_('is EU member'), default=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name.lower())
        super().save(*args, **kwargs)


class City(models.Model):
    """Cities within countries"""
    
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    population = models.PositiveIntegerField(_('population'), null=True, blank=True)
    is_capital = models.BooleanField(_('is capital'), default=False)
    
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['country__name', 'name']
        unique_together = [['name', 'country'], ['slug', 'country']]
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name.lower())
            self.slug = base_slug
            
            # Ensure uniqueness within the same country
            counter = 1
            while City.objects.filter(slug=self.slug, country=self.country).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)


class Business(models.Model):
    """Business listings"""
    
    PLAN_CHOICES = [
        ('free', _('Free Listing')),
        ('local', _('Local Plan')),
        ('country', _('Country Plan')),
        ('eu', _('EU Plan')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending Approval')),
        ('active', _('Active')),
        ('suspended', _('Suspended')),
        ('expired', _('Expired')),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    
    # Business Details
    name = models.CharField(_('business name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    short_description = models.CharField(_('short description'), max_length=300, blank=True)
    
    # Contact Information
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    website = models.URLField(_('website'), blank=True)
    
    # Location
    address = models.TextField(_('address'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='businesses')
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Business Classification
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='businesses')
    subcategories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='subcategory_businesses',
        limit_choices_to={'parent__isnull': False}
    )
    
    # Media
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='business_covers/', blank=True, null=True)
    
    # Business Hours
    monday_hours = models.CharField(_('Monday hours'), max_length=50, blank=True)
    tuesday_hours = models.CharField(_('Tuesday hours'), max_length=50, blank=True)
    wednesday_hours = models.CharField(_('Wednesday hours'), max_length=50, blank=True)
    thursday_hours = models.CharField(_('Thursday hours'), max_length=50, blank=True)
    friday_hours = models.CharField(_('Friday hours'), max_length=50, blank=True)
    saturday_hours = models.CharField(_('Saturday hours'), max_length=50, blank=True)
    sunday_hours = models.CharField(_('Sunday hours'), max_length=50, blank=True)
    
    # Subscription & Status
    plan = models.CharField(_('plan'), max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    featured = models.BooleanField(_('featured'), default=False)
    verified = models.BooleanField(_('verified'), default=False)
    
    # SEO & Marketing
    meta_title = models.CharField(_('meta title'), max_length=60, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=160, blank=True)
    keywords = models.CharField(_('keywords'), max_length=500, blank=True)
    
    # Statistics
    views_count = models.PositiveIntegerField(_('views count'), default=0)
    clicks_count = models.PositiveIntegerField(_('clicks count'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    expires_at = models.DateTimeField(_('expires at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'plan']),
            models.Index(fields=['city', 'category']),
            models.Index(fields=['featured', 'verified']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0
    
    @property
    def review_count(self):
        """Count approved reviews"""
        return self.reviews.filter(is_approved=True).count()
    
    def save(self, *args, **kwargs):
        if self.status == 'active' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class BusinessImage(models.Model):
    """Additional images for businesses"""
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business_images/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Business Image')
        verbose_name_plural = _('Business Images')
        ordering = ['sort_order', '-created_at']
    
    def __str__(self):
        return f"{self.business.name} - Image {self.id}"


class Review(models.Model):
    """Customer reviews for businesses"""
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    
    # Moderation
    is_approved = models.BooleanField(_('is approved'), default=False)
    moderation_notes = models.TextField(_('moderation notes'), blank=True)
    
    # Response from business owner
    owner_response = models.TextField(_('owner response'), blank=True)
    response_date = models.DateTimeField(_('response date'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        unique_together = ['business', 'reviewer']  # One review per user per business
    
    def __str__(self):
        return f"{self.business.name} - {self.rating} stars by {self.reviewer.full_name}"


# Import registration models
from .models_registration import BusinessRegistration, BusinessPhoto, BusinessClaim