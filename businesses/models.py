from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
import uuid
import re

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
        constraints = [
            # Prevent exact duplicates: same name and city
            models.UniqueConstraint(
                fields=['name', 'city'], 
                name='unique_business_name_city'
            ),
            # Prevent same email in same city (common duplicate pattern)
            models.UniqueConstraint(
                fields=['email', 'city'],
                name='unique_business_email_city',
                condition=models.Q(email__isnull=False) & ~models.Q(email='')
            ),
            # Prevent same phone in same city
            models.UniqueConstraint(
                fields=['phone', 'city'],
                name='unique_business_phone_city', 
                condition=models.Q(phone__isnull=False) & ~models.Q(phone='')
            ),
        ]
        indexes = [
            models.Index(fields=['status', 'plan']),
            models.Index(fields=['city', 'category']),
            models.Index(fields=['featured', 'verified']),
            models.Index(fields=['name', 'city']),  # For duplicate checking
            models.Index(fields=['email', 'city']),  # For duplicate checking
            models.Index(fields=['phone', 'city']),  # For duplicate checking
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
    
    def clean(self):
        """Validate business data to prevent duplicates"""
        super().clean()
        
        # Normalize name for comparison
        if self.name:
            self.name = self.normalize_business_name(self.name)
            
        # Check for potential duplicates
        self.check_for_duplicates()
    
    def normalize_business_name(self, name):
        """Normalize business name for consistent comparison"""
        if not name:
            return name
            
        # Remove extra spaces and standardize
        name = re.sub(r'\s+', ' ', name.strip())
        
        # Remove common business suffixes that might cause duplicates
        suffixes = ['ltd', 'limited', 'inc', 'incorporated', 'llc', 'corp', 'corporation', 
                   'gmbh', 'sa', 'srl', 'bv', 'oy', 'ab', 'as']
        
        for suffix in suffixes:
            # Remove suffix with various separators
            patterns = [
                rf'\s+{re.escape(suffix)}\s*$',  # " ltd"
                rf'[,.\s]+{re.escape(suffix)}\s*$',  # ", ltd" or ". ltd"
                rf'\s*\({re.escape(suffix)}\)\s*$',  # " (ltd)"
            ]
            for pattern in patterns:
                name = re.sub(pattern, '', name, flags=re.IGNORECASE)
                
        return name.strip()
    
    def check_for_duplicates(self):
        """Check for potential duplicates and raise validation error"""
        if not self.name or not self.city:
            return
            
        # Get existing businesses to check against
        existing_qs = Business.objects.filter(city=self.city)
        if self.pk:
            existing_qs = existing_qs.exclude(pk=self.pk)
            
        # Check for exact name match (case insensitive)
        if existing_qs.filter(name__iexact=self.name).exists():
            raise ValidationError({
                'name': 'A business with this name already exists in this city.'
            })
            
        # Check for similar names (fuzzy matching)
        similar_names = self.find_similar_names(existing_qs)
        if similar_names:
            raise ValidationError({
                'name': f'Similar business names found in this city: {", ".join(similar_names)}. '
                       'Please use a more distinctive name or verify this is not a duplicate.'
            })
            
        # Check for same email
        if self.email and existing_qs.filter(email__iexact=self.email).exists():
            raise ValidationError({
                'email': 'A business with this email already exists in this city.'
            })
            
        # Check for same phone
        if self.phone and existing_qs.filter(phone=self.phone).exists():
            raise ValidationError({
                'phone': 'A business with this phone number already exists in this city.'
            })
    
    def find_similar_names(self, queryset):
        """Find businesses with similar names using fuzzy matching"""
        similar_names = []
        current_name = self.name.lower().strip()
        
        # Split into words for comparison
        current_words = set(re.findall(r'\b\w+\b', current_name))
        
        for business in queryset.only('name'):
            existing_name = business.name.lower().strip()
            existing_words = set(re.findall(r'\b\w+\b', existing_name))
            
            # Calculate similarity
            if current_words and existing_words:
                intersection = current_words.intersection(existing_words)
                union = current_words.union(existing_words)
                similarity = len(intersection) / len(union)
                
                # If similarity > 80% and names share significant words
                if (similarity > 0.8 and len(intersection) >= 2) or \
                   (similarity > 0.9 and len(intersection) >= 1):
                    similar_names.append(business.name)
                    
                # Also check if one name is contained in another
                if (current_name in existing_name or existing_name in current_name) and \
                   abs(len(current_name) - len(existing_name)) <= 5:
                    similar_names.append(business.name)
                    
        return similar_names[:3]  # Limit to 3 examples
    
    @classmethod
    def check_potential_duplicate(cls, name, city, email=None, phone=None, exclude_id=None):
        """Class method to check for potential duplicates before creating"""
        issues = []
        
        qs = cls.objects.filter(city=city)
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
            
        # Normalize the name
        normalized_name = cls().normalize_business_name(name) if name else ''
        
        # Check name duplicates
        if normalized_name:
            if qs.filter(name__iexact=normalized_name).exists():
                issues.append('Exact name match found')
            else:
                # Check for similar names
                temp_business = cls(name=normalized_name, city=city)
                similar = temp_business.find_similar_names(qs)
                if similar:
                    issues.append(f'Similar names found: {", ".join(similar)}')
                    
        # Check email duplicates
        if email and qs.filter(email__iexact=email).exists():
            issues.append('Email already exists in this city')
            
        # Check phone duplicates  
        if phone and qs.filter(phone=phone).exists():
            issues.append('Phone number already exists in this city')
            
        return issues
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        # Run full validation before saving
        self.full_clean()
        
        # Set published date for active businesses
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