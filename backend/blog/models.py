from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Hex color code')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('nl', 'Dutch'),
        ('pl', 'Polish'),
        ('ro', 'Romanian'),
        ('cs', 'Czech'),
        ('hu', 'Hungarian'),
        ('bg', 'Bulgarian'),
        ('hr', 'Croatian'),
        ('sk', 'Slovak'),
        ('sl', 'Slovenian'),
        ('et', 'Estonian'),
        ('lv', 'Latvian'),
        ('lt', 'Lithuanian'),
        ('fi', 'Finnish'),
        ('sv', 'Swedish'),
        ('da', 'Danish'),
        ('el', 'Greek'),
        ('mt', 'Maltese'),
        ('ga', 'Irish'),
        ('cy', 'Welsh'),
        ('lb', 'Luxembourgish'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    
    excerpt = models.TextField(max_length=300, help_text='Brief description for previews')
    content = RichTextUploadingField(config_name='blog', help_text='Main blog post content with rich text formatting')
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True, help_text='Alt text for SEO')
    
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=0, help_text='Estimated read time in minutes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['language', 'status']),
            models.Index(fields=['featured', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.language}")
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        if not self.meta_title:
            self.meta_title = self.title[:60]
        
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        
        # Calculate read time (average 200 words per minute)
        word_count = len(self.content.split())
        self.read_time = max(1, word_count // 200)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug, 'lang': self.language})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def __str__(self):
        return f"{self.title} ({self.language})"


class PricingPlan(models.Model):
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ]
    
    CURRENCY_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
        ('GBP', 'British Pound'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLE_CHOICES, default='monthly')
    
    # Features
    features = models.JSONField(default=list, help_text='List of features included in this plan')
    max_listings = models.PositiveIntegerField(default=1, help_text='Maximum number of business listings')
    max_images = models.PositiveIntegerField(default=5, help_text='Maximum images per listing')
    priority_support = models.BooleanField(default=False)
    
    # Display settings
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Highlight this plan')
    color_scheme = models.CharField(max_length=20, default='blue', 
                                   choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), ('gold', 'Gold')])
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers first)')
    
    # Trial and promotional
    trial_days = models.PositiveIntegerField(default=0, help_text='Free trial period in days')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'
        ordering = ['order', 'price']
    
    def get_display_price(self):
        if self.price == 0:
            return 'Free'
        return f"{self.currency} {self.price}"
    
    def get_billing_display(self):
        if self.billing_cycle == 'monthly':
            return f"{self.get_display_price()}/month"
        elif self.billing_cycle == 'yearly':
            return f"{self.get_display_price()}/year"
        else:
            return self.get_display_price()
    
    def __str__(self):
        return f"{self.name} - {self.get_billing_display()}"


class BusinessSubscription(models.Model):
    """Track business subscriptions to pricing plans"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('trial', 'Trial'),
    ]
    
    business = models.ForeignKey('catalog.Business', on_delete=models.CASCADE, related_name='subscriptions')
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='subscriptions')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='trial')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    
    # Payment tracking
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Business Subscription'
        verbose_name_plural = 'Business Subscriptions'
        ordering = ['-created_at']
    
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()
    
    def __str__(self):
        return f"{self.business.name} - {self.pricing_plan.name} ({self.status})"