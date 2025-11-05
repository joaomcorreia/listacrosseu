from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.models.seo import SEOMixin


class Category(SEOMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))
    name_en = models.CharField(max_length=100, verbose_name=_('Name (English)'), blank=True)
    name_fr = models.CharField(max_length=100, verbose_name=_('Name (French)'), blank=True)
    name_nl = models.CharField(max_length=100, verbose_name=_('Name (Dutch)'), blank=True)
    name_pt = models.CharField(max_length=100, verbose_name=_('Name (Portuguese)'), blank=True)
    name_de = models.CharField(max_length=100, verbose_name=_('Name (German)'), blank=True)
    name_es = models.CharField(max_length=100, verbose_name=_('Name (Spanish)'), blank=True)
    name_ar = models.CharField(max_length=100, verbose_name=_('Name (Arabic)'), blank=True)
    
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_name_for_language(self, language_code):
        """Get category name in specific language"""
        if language_code == 'en' and self.name_en:
            return self.name_en
        elif language_code == 'fr' and self.name_fr:
            return self.name_fr
        elif language_code == 'nl' and self.name_nl:
            return self.name_nl
        elif language_code == 'pt' and self.name_pt:
            return self.name_pt
        elif language_code == 'de' and self.name_de:
            return self.name_de
        elif language_code == 'es' and self.name_es:
            return self.name_es
        elif language_code == 'ar' and self.name_ar:
            return self.name_ar
        return self.name


class Business(SEOMixin, models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Business Name'))
    description = models.TextField(verbose_name=_('Description'))
    description_en = models.TextField(verbose_name=_('Description (English)'), blank=True)
    description_fr = models.TextField(verbose_name=_('Description (French)'), blank=True)
    description_nl = models.TextField(verbose_name=_('Description (Dutch)'), blank=True)
    description_pt = models.TextField(verbose_name=_('Description (Portuguese)'), blank=True)
    description_de = models.TextField(verbose_name=_('Description (German)'), blank=True)
    description_es = models.TextField(verbose_name=_('Description (Spanish)'), blank=True)
    description_ar = models.TextField(verbose_name=_('Description (Arabic)'), blank=True)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Owner'))
    
    # Contact Information
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    
    # Address
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    country = models.CharField(max_length=100, verbose_name=_('Country'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Opening Hours
    monday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Monday Hours'))
    tuesday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Tuesday Hours'))
    wednesday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Wednesday Hours'))
    thursday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Thursday Hours'))
    friday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Friday Hours'))
    saturday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Saturday Hours'))
    sunday_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Sunday Hours'))
    
    # Import tracking
    imported_from_csv = models.BooleanField(default=False, verbose_name=_('Imported from CSV'))
    csv_import_date = models.DateTimeField(null=True, blank=True, verbose_name=_('CSV Import Date'))
    google_place_id = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Google Place ID'))
    google_import_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Google Import Date'))
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    is_public = models.BooleanField(default=True, verbose_name=_('Is Public'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Is Featured'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))
    
    # SEO
    slug = models.SlugField(unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_description_for_language(self, language_code):
        """Get business description in specific language"""
        if language_code == 'en' and self.description_en:
            return self.description_en
        elif language_code == 'fr' and self.description_fr:
            return self.description_fr
        elif language_code == 'nl' and self.description_nl:
            return self.description_nl
        elif language_code == 'pt' and self.description_pt:
            return self.description_pt
        elif language_code == 'de' and self.description_de:
            return self.description_de
        elif language_code == 'es' and self.description_es:
            return self.description_es
        elif language_code == 'ar' and self.description_ar:
            return self.description_ar
        return self.description


class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business_images/')
    caption = models.CharField(max_length=200, blank=True, verbose_name=_('Caption'))
    is_primary = models.BooleanField(default=False, verbose_name=_('Is Primary'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Business Image')
        verbose_name_plural = _('Business Images')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"Image for {self.business.name}"


class CSVUpload(models.Model):
    """Model to track CSV file uploads for business data"""
    
    PROCESSING_STATUS = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]
    
    file = models.FileField(upload_to='csv_uploads/', verbose_name=_('CSV File'))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Uploaded By'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Uploaded At'))
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Processed At'))
    
    status = models.CharField(
        max_length=20, 
        choices=PROCESSING_STATUS, 
        default='pending',
        verbose_name=_('Processing Status')
    )
    
    total_rows = models.PositiveIntegerField(default=0, verbose_name=_('Total Rows'))
    processed_rows = models.PositiveIntegerField(default=0, verbose_name=_('Processed Rows'))
    successful_rows = models.PositiveIntegerField(default=0, verbose_name=_('Successful Rows'))
    failed_rows = models.PositiveIntegerField(default=0, verbose_name=_('Failed Rows'))
    
    error_log = models.TextField(blank=True, verbose_name=_('Error Log'))
    processing_notes = models.TextField(blank=True, verbose_name=_('Processing Notes'))
    
    class Meta:
        verbose_name = _('CSV Upload')
        verbose_name_plural = _('CSV Uploads')
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"CSV Upload - {self.file.name} ({self.status})"
    
    def mark_as_processing(self):
        """Mark the upload as currently being processed"""
        self.status = 'processing'
        self.save()
    
    def mark_as_completed(self, successful_count, failed_count):
        """Mark the upload as completed with statistics"""
        self.status = 'completed'
        self.processed_at = timezone.now()
        self.successful_rows = successful_count
        self.failed_rows = failed_count
        self.processed_rows = successful_count + failed_count
        self.save()
    
    def mark_as_failed(self, error_message):
        """Mark the upload as failed with error message"""
        self.status = 'failed'
        self.processed_at = timezone.now()
        self.error_log = error_message
        self.save()