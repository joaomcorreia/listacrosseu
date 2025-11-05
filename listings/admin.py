from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from core.admin.seo_admin import SEOFirstAdmin
from .models import Category, Business, BusinessImage, CSVUpload
from .services.csv_processor import process_csv_upload


@admin.register(Category)
class CategoryAdmin(SEOFirstAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_en', 'name_fr', 'name_nl', 'name_pt', 'name_de', 'name_es', 'name_ar']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        SEOFirstAdmin.seo_fieldset,  # SEO at top with live preview
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        (_('Translations'), {
            'fields': ('name_en', 'name_fr', 'name_nl', 'name_pt', 'name_de', 'name_es', 'name_ar'),
            'classes': ('collapse',)
        }),
    )


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']


@admin.register(Business)
class BusinessAdmin(SEOFirstAdmin):
    list_display = ['name', 'category', 'city', 'country', 'is_active', 'is_featured', 'is_verified', 'imported_from_csv', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'is_verified', 'is_public', 'imported_from_csv', 'country', 'created_at']
    search_fields = ['name', 'description', 'email', 'city', 'country']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BusinessImageInline]
    
    fieldsets = (
        SEOFirstAdmin.seo_fieldset,  # SEO at top with live preview
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'category', 'owner')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'website')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'country', 'postal_code', 'latitude', 'longitude')
        }),
        (_('Opening Hours'), {
            'fields': ('monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_public', 'is_featured', 'is_verified')
        }),
        (_('Import Information'), {
            'fields': ('imported_from_csv', 'csv_import_date'),
            'classes': ('collapse',)
        }),
        (_('Translations'), {
            'fields': ('description_en', 'description_fr', 'description_nl', 'description_pt', 'description_de', 'description_es', 'description_ar'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'owner')


@admin.register(BusinessImage)
class BusinessImageAdmin(admin.ModelAdmin):
    list_display = ['business', 'caption', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['business__name', 'caption']


@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_by', 'status', 'total_rows', 'successful_rows', 'failed_rows', 'uploaded_at', 'processed_at']
    list_filter = ['status', 'uploaded_at', 'processed_at', 'uploaded_by']
    search_fields = ['file', 'uploaded_by__username']
    readonly_fields = ['uploaded_at', 'processed_at', 'total_rows', 'processed_rows', 'successful_rows', 'failed_rows']
    actions = ['process_csv_files', 'reprocess_failed_csvs']
    
    fieldsets = (
        (_('File Information'), {
            'fields': ('file', 'uploaded_by', 'uploaded_at')
        }),
        (_('Processing Status'), {
            'fields': ('status', 'processed_at', 'total_rows', 'processed_rows', 'successful_rows', 'failed_rows')
        }),
        (_('Logs and Notes'), {
            'fields': ('error_log', 'processing_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def file_name(self, obj):
        """Display just the filename, not the full path"""
        return obj.file.name.split('/')[-1] if obj.file else '-'
    file_name.short_description = 'File Name'
    
    def process_csv_files(self, request, queryset):
        """Admin action to process selected CSV files"""
        processed_count = 0
        for csv_upload in queryset.filter(status='pending'):
            try:
                result = process_csv_upload(csv_upload.id)
                if result['success']:
                    processed_count += 1
                    self.message_user(
                        request,
                        f"Successfully processed {csv_upload.file.name}: {result['successful_count']} businesses imported."
                    )
                else:
                    self.message_user(
                        request,
                        f"Failed to process {csv_upload.file.name}: {result['message']}",
                        level='ERROR'
                    )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error processing {csv_upload.file.name}: {str(e)}",
                    level='ERROR'
                )
        
        if processed_count:
            self.message_user(request, f"Successfully processed {processed_count} CSV files.")
    
    process_csv_files.short_description = "Process selected CSV files"
    
    def reprocess_failed_csvs(self, request, queryset):
        """Admin action to reprocess failed CSV files"""
        reprocessed_count = 0
        for csv_upload in queryset.filter(status='failed'):
            try:
                # Reset status to pending
                csv_upload.status = 'pending'
                csv_upload.error_log = ''
                csv_upload.processed_at = None
                csv_upload.save()
                
                # Process again
                result = process_csv_upload(csv_upload.id)
                if result['success']:
                    reprocessed_count += 1
                    self.message_user(
                        request,
                        f"Successfully reprocessed {csv_upload.file.name}: {result['successful_count']} businesses imported."
                    )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error reprocessing {csv_upload.file.name}: {str(e)}",
                    level='ERROR'
                )
        
        if reprocessed_count:
            self.message_user(request, f"Successfully reprocessed {reprocessed_count} CSV files.")
    
    reprocess_failed_csvs.short_description = "Reprocess failed CSV files"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('uploaded_by')