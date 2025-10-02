from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ImportJob, ImportMapping
import json


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'original_filename', 'file_type', 'status',
        'progress_display', 'total_records', 'successful_records',
        'failed_records', 'created_at', 'view_details_link'
    ]
    list_filter = ['status', 'file_type', 'created_at']
    search_fields = ['user__email', 'original_filename']
    readonly_fields = [
        'created_at', 'updated_at', 'started_at', 'completed_at',
        'file_path', 'progress', 'total_records', 'processed_records',
        'successful_records', 'failed_records'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'original_filename', 'file_type', 'status')
        }),
        ('File Information', {
            'fields': ('file_path', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Import Configuration', {
            'fields': ('mapping', 'options_display'),
            'classes': ('collapse',)
        }),
        ('Progress Tracking', {
            'fields': (
                'progress', 'total_records', 'processed_records',
                'successful_records', 'failed_records'
            ),
        }),
        ('Timing', {
            'fields': ('created_at', 'started_at', 'completed_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message', 'error_details_display'),
            'classes': ('collapse',)
        }),
    )
    
    def progress_display(self, obj):
        if obj.total_records > 0:
            percentage = (obj.processed_records / obj.total_records) * 100
            return format_html(
                '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
                '<div style="width: {}%; height: 20px; background-color: #28a745; border-radius: 3px;"></div>'
                '</div>'
                '<small>{}%</small>',
                percentage, round(percentage, 1)
            )
        return 'N/A'
    progress_display.short_description = 'Progress'
    
    def view_details_link(self, obj):
        return format_html(
            '<a href="{}">View Details</a>',
            reverse('admin:data_import_importjob_change', args=[obj.pk])
        )
    view_details_link.short_description = 'Details'
    
    def options_display(self, obj):
        if obj.options:
            return format_html(
                '<pre>{}</pre>',
                json.dumps(obj.options, indent=2)
            )
        return 'No options'
    options_display.short_description = 'Options'
    
    def error_details_display(self, obj):
        if obj.error_details:
            return format_html(
                '<pre>{}</pre>',
                json.dumps(obj.error_details, indent=2)
            )
        return 'No error details'
    error_details_display.short_description = 'Error Details'
    
    actions = ['cancel_jobs', 'retry_failed_jobs']
    
    def cancel_jobs(self, request, queryset):
        count = 0
        for job in queryset:
            if job.status in ['pending', 'processing']:
                job.status = 'cancelled'
                job.save()
                count += 1
        
        self.message_user(request, f'{count} import jobs cancelled.')
    cancel_jobs.short_description = 'Cancel selected import jobs'
    
    def retry_failed_jobs(self, request, queryset):
        count = 0
        for job in queryset.filter(status='failed'):
            job.status = 'pending'
            job.error_message = ''
            job.error_details = {}
            job.progress = 0
            job.processed_records = 0
            job.save()
            count += 1
        
        self.message_user(request, f'{count} failed import jobs queued for retry.')
    retry_failed_jobs.short_description = 'Retry failed import jobs'


@admin.register(ImportMapping)
class ImportMappingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_default', 'created_at']
    list_filter = ['is_default', 'created_at']
    search_fields = ['name', 'user__email', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'is_default')
        }),
        ('Mapping Configuration', {
            'fields': ('mapping_display',),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mapping_display(self, obj):
        return format_html(
            '<pre>{}</pre>',
            json.dumps(obj.mapping, indent=2)
        )
    mapping_display.short_description = 'Field Mapping'
    
    actions = ['set_as_default', 'unset_as_default']
    
    def set_as_default(self, request, queryset):
        # First unset all defaults for each user
        for mapping in queryset:
            ImportMapping.objects.filter(
                user=mapping.user, is_default=True
            ).update(is_default=False)
            
            mapping.is_default = True
            mapping.save()
        
        count = queryset.count()
        self.message_user(request, f'{count} mappings set as default.')
    set_as_default.short_description = 'Set as default mapping'
    
    def unset_as_default(self, request, queryset):
        count = queryset.update(is_default=False)
        self.message_user(request, f'{count} mappings unset as default.')
    unset_as_default.short_description = 'Remove default status'