from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid

User = get_user_model()


class Domain(models.Model):
    """Available domains for user websites"""
    
    STATUS_CHOICES = [
        ('available', _('Available')),
        ('reserved', _('Reserved')),
        ('active', _('Active')),
        ('suspended', _('Suspended')),
    ]
    
    domain_name = models.CharField(
        _('domain name'),
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.listacross\.eu$',
                message=_('Domain must be in format: yourname.listacross.eu')
            )
        ]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='domains',
        null=True,
        blank=True
    )
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='available')
    
    # DNS settings
    is_ssl_enabled = models.BooleanField(_('SSL enabled'), default=True)
    dns_configured = models.BooleanField(_('DNS configured'), default=False)
    
    # Metadata
    reserved_at = models.DateTimeField(_('reserved at'), null=True, blank=True)
    activated_at = models.DateTimeField(_('activated at'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')
        ordering = ['domain_name']
    
    def __str__(self):
        return self.domain_name
    
    @property
    def subdomain(self):
        """Extract subdomain from full domain"""
        return self.domain_name.split('.')[0]
    
    def is_available(self):
        return self.status == 'available'


class Website(models.Model):
    """User websites for EU plan subscribers"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('suspended', _('Suspended')),
    ]
    
    THEME_CHOICES = [
        ('modern', _('Modern Business')),
        ('classic', _('Classic Professional')),
        ('minimal', _('Minimal Clean')),
        ('creative', _('Creative Portfolio')),
        ('corporate', _('Corporate Blue')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='website')
    domain = models.OneToOneField(Domain, on_delete=models.CASCADE, related_name='website')
    
    # Website Configuration
    title = models.CharField(_('website title'), max_length=100)
    tagline = models.CharField(_('tagline'), max_length=200, blank=True)
    description = models.TextField(_('description'), blank=True)
    theme = models.CharField(_('theme'), max_length=20, choices=THEME_CHOICES, default='modern')
    
    # Branding
    logo = models.ImageField(upload_to='website_logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='website_favicons/', blank=True, null=True)
    primary_color = models.CharField(_('primary color'), max_length=7, default='#1e40af')  # Hex color
    secondary_color = models.CharField(_('secondary color'), max_length=7, default='#64748b')
    
    # Content
    about_text = models.TextField(_('about text'), blank=True)
    services_text = models.TextField(_('services text'), blank=True)
    contact_text = models.TextField(_('contact text'), blank=True)
    
    # Contact Information
    contact_email = models.EmailField(_('contact email'), blank=True)
    contact_phone = models.CharField(_('contact phone'), max_length=20, blank=True)
    contact_address = models.TextField(_('contact address'), blank=True)
    
    # Social Media
    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    twitter_url = models.URLField(_('Twitter URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    
    # SEO
    meta_title = models.CharField(_('meta title'), max_length=60, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=160, blank=True)
    keywords = models.CharField(_('keywords'), max_length=500, blank=True)
    
    # Settings
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    show_business_listings = models.BooleanField(_('show business listings'), default=True)
    show_contact_form = models.BooleanField(_('show contact form'), default=True)
    show_social_links = models.BooleanField(_('show social links'), default=True)
    
    # Analytics
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=50, blank=True)
    
    # Statistics
    page_views = models.PositiveIntegerField(_('page views'), default=0)
    unique_visitors = models.PositiveIntegerField(_('unique visitors'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Website')
        verbose_name_plural = _('Websites')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.domain.domain_name})"
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def url(self):
        protocol = 'https' if self.domain.is_ssl_enabled else 'http'
        return f"{protocol}://{self.domain.domain_name}"
    
    def publish(self):
        """Publish the website"""
        self.status = 'published'
        if not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the website"""
        self.status = 'draft'
        self.save()


class WebsitePage(models.Model):
    """Additional pages for user websites"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
    ]
    
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    
    # Page details
    title = models.CharField(_('page title'), max_length=100)
    slug = models.SlugField(_('slug'))
    content = models.TextField(_('content'))
    
    # SEO
    meta_title = models.CharField(_('meta title'), max_length=60, blank=True)
    meta_description = models.CharField(_('meta description'), max_length=160, blank=True)
    
    # Settings
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    show_in_menu = models.BooleanField(_('show in menu'), default=True)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Website Page')
        verbose_name_plural = _('Website Pages')
        ordering = ['sort_order', 'title']
        unique_together = ['website', 'slug']
    
    def __str__(self):
        return f"{self.website.title} - {self.title}"
    
    @property
    def url(self):
        return f"{self.website.url}/{self.slug}/"


class WebsiteImage(models.Model):
    """Images for user websites"""
    
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='images')
    
    image = models.ImageField(upload_to='website_images/')
    alt_text = models.CharField(_('alt text'), max_length=200, blank=True)
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    
    # Usage
    is_gallery_image = models.BooleanField(_('gallery image'), default=False)
    is_hero_image = models.BooleanField(_('hero image'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Website Image')
        verbose_name_plural = _('Website Images')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.website.title} - {self.image.name}"


class ContactSubmission(models.Model):
    """Contact form submissions from user websites"""
    
    STATUS_CHOICES = [
        ('new', _('New')),
        ('read', _('Read')),
        ('replied', _('Replied')),
        ('archived', _('Archived')),
    ]
    
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='contact_submissions')
    
    # Submission details
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    subject = models.CharField(_('subject'), max_length=200)
    message = models.TextField(_('message'))
    
    # Metadata
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)
    
    # Admin response
    admin_notes = models.TextField(_('admin notes'), blank=True)
    replied_at = models.DateTimeField(_('replied at'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Contact Submission')
        verbose_name_plural = _('Contact Submissions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.website.title} - {self.name} ({self.subject})"
    
    def mark_as_read(self):
        if self.status == 'new':
            self.status = 'read'
            self.save()
    
    def mark_as_replied(self):
        self.status = 'replied'
        from django.utils import timezone
        self.replied_at = timezone.now()
        self.save()