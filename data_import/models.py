from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class DataSource(models.Model):
    """External data sources for importing business listings"""
    
    SOURCE_TYPES = [
        ('csv', _('CSV File')),
        ('json', _('JSON File')),
        ('api', _('API Endpoint')),
        ('openstreetmap', _('OpenStreetMap')),
        ('google_places', _('Google Places')),
        ('yelp', _('Yelp API')),
        ('foursquare', _('Foursquare API')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('error', _('Error')),
    ]
    
    name = models.CharField(_('name'), max_length=100)
    source_type = models.CharField(_('source type'), max_length=20, choices=SOURCE_TYPES)
    description = models.TextField(_('description'), blank=True)
    
    # Configuration
    endpoint_url = models.URLField(_('endpoint URL'), blank=True)
    api_key = models.CharField(_('API key'), max_length=200, blank=True)
    headers = models.JSONField(_('headers'), default=dict, blank=True)
    
    # File uploads
    csv_file = models.FileField(upload_to='data_imports/csv/', blank=True, null=True)
    json_file = models.FileField(upload_to='data_imports/json/', blank=True, null=True)
    
    # Field mapping
    field_mapping = models.JSONField(_('field mapping'), default=dict, help_text=_('Map source fields to our business model fields'))
    
    # Settings
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    auto_import = models.BooleanField(_('auto import'), default=False)
    import_frequency = models.PositiveIntegerField(_('import frequency (hours)'), default=24)
    
    # Statistics
    last_import = models.DateTimeField(_('last import'), null=True, blank=True)
    total_imported = models.PositiveIntegerField(_('total imported'), default=0)
    last_error = models.TextField(_('last error'), blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Data Source')
        verbose_name_plural = _('Data Sources')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"



    
    def mark_started(self):
        """Mark job as started"""
        from django.utils import timezone
        self.status = 'running'
        self.started_at = timezone.now()
        self.save()
    
    def mark_completed(self):
        """Mark job as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_failed(self, error_message):
        """Mark job as failed"""
        from django.utils import timezone
        self.status = 'failed'
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save()


class ImportRecord(models.Model):
    """Individual import record details"""
    
    STATUS_CHOICES = [
        ('success', _('Success')),
        ('failed', _('Failed')),
        ('skipped', _('Skipped')),
        ('duplicate', _('Duplicate')),
    ]
    
    import_job = models.ForeignKey('ImportJob', on_delete=models.CASCADE, related_name='records')
    
    # Source data
    source_id = models.CharField(_('source ID'), max_length=100, blank=True)
    source_data = models.JSONField(_('source data'), default=dict)
    
    # Import result
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(_('error message'), blank=True)
    
    # Created business (if successful)
    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='import_records'
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Import Record')
        verbose_name_plural = _('Import Records')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['import_job', 'status']),
            models.Index(fields=['source_id']),
        ]
    
    def __str__(self):
        return f"Record {self.id} - {self.status}"


class DataTemplate(models.Model):
    """Templates for data import field mapping"""
    
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    source_type = models.CharField(_('source type'), max_length=20, choices=DataSource.SOURCE_TYPES)
    
    # Template configuration
    field_mapping = models.JSONField(_('field mapping'), default=dict)
    validation_rules = models.JSONField(_('validation rules'), default=dict)
    transformation_rules = models.JSONField(_('transformation rules'), default=dict)
    
    # Sample data
    sample_input = models.JSONField(_('sample input'), default=dict, blank=True)
    sample_output = models.JSONField(_('sample output'), default=dict, blank=True)
    
    # Settings
    is_active = models.BooleanField(_('is active'), default=True)
    is_default = models.BooleanField(_('is default'), default=False)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Data Template')
        verbose_name_plural = _('Data Templates')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class ImportMapping(models.Model):
    """Field mappings for data imports"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    # Mapping configuration
    mapping = models.JSONField(_('field mapping'), default=dict, help_text=_('JSON mapping of source fields to target fields'))
    
    # Settings
    is_default = models.BooleanField(_('is default'), default=False)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Import Mapping')
        verbose_name_plural = _('Import Mappings')
        ordering = ['name']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"


class ImportJob(models.Model):
    """Import job tracking"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(_('file path'), max_length=500)
    file_type = models.CharField(_('file type'), max_length=10, choices=[('csv', 'CSV'), ('json', 'JSON')])
    original_filename = models.CharField(_('original filename'), max_length=255)
    
    # Configuration
    mapping = models.ForeignKey(ImportMapping, on_delete=models.SET_NULL, null=True, blank=True)
    options = models.JSONField(_('options'), default=dict, blank=True)
    
    # Status tracking
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.PositiveIntegerField(_('progress'), default=0)  # Percentage
    
    # Statistics
    total_records = models.PositiveIntegerField(_('total records'), default=0)
    processed_records = models.PositiveIntegerField(_('processed records'), default=0)
    successful_records = models.PositiveIntegerField(_('successful records'), default=0)
    failed_records = models.PositiveIntegerField(_('failed records'), default=0)
    
    # Error handling
    error_message = models.TextField(_('error message'), blank=True)
    error_details = models.JSONField(_('error details'), default=dict, blank=True)
    
    # File information
    file_size = models.PositiveIntegerField(_('file size (bytes)'), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    started_at = models.DateTimeField(_('started at'), null=True, blank=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Import Job')
        verbose_name_plural = _('Import Jobs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_filename} - {self.get_status_display()}"