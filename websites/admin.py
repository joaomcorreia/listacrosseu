from django.contrib import admin
from django.utils.html import format_html
from .models import Website, Domain, ContactSubmission


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'domain', 'status', 'theme', 
        'created_at', 'view_website_link'
    ]
    list_filter = ['status', 'theme', 'created_at']
    search_fields = ['title', 'user__email', 'domain__domain_name']
    readonly_fields = ['created_at', 'updated_at', 'page_views', 'unique_visitors']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'domain', 'title', 'tagline', 'description')
        }),
        ('Content', {
            'fields': ('about_text', 'services_text', 'contact_text'),
            'classes': ('collapse',)
        }),
        ('Design', {
            'fields': ('theme', 'primary_color', 'secondary_color'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('logo', 'favicon'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status', 'show_business_listings', 'show_contact_form', 'show_social_links', 'google_analytics_id'),
        }),
        ('Statistics', {
            'fields': ('page_views', 'unique_visitors', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def view_website_link(self, obj):
        if obj.status == 'published':
            return format_html(
                '<a href="https://{}" target="_blank">View Website</a>',
                obj.domain.domain_name
            )
        return 'Not Published'
    view_website_link.short_description = 'Website'
    
    actions = ['publish_websites', 'unpublish_websites']
    
    def publish_websites(self, request, queryset):
        count = queryset.filter(status='draft').update(status='published')
        self.message_user(request, f'{count} websites published.')
    publish_websites.short_description = 'Publish selected websites'
    
    def unpublish_websites(self, request, queryset):
        count = queryset.update(status='draft')
        self.message_user(request, f'{count} websites unpublished.')
    unpublish_websites.short_description = 'Unpublish selected websites'


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'status', 'user', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['domain_name', 'user__email']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Domain Information', {
            'fields': ('domain_name', 'status', 'user')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_available', 'mark_reserved']
    
    def mark_available(self, request, queryset):
        count = queryset.update(status='available', user=None)
        self.message_user(request, f'{count} domains marked as available.')
    mark_available.short_description = 'Mark selected domains as available'
    
    def mark_reserved(self, request, queryset):
        count = queryset.update(status='reserved')
        self.message_user(request, f'{count} domains marked as reserved.')
    mark_reserved.short_description = 'Mark selected domains as reserved'


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'website', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'website']
    search_fields = ['name', 'email', 'subject', 'website__title']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'website')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'status')
        }),
        ('Admin Response', {
            'fields': ('admin_notes', 'replied_at'),
            'classes': ('collapse',)
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(status='read')
        self.message_user(request, f'{count} submissions marked as read.')
    mark_as_read.short_description = 'Mark selected submissions as read'
    
    def mark_as_replied(self, request, queryset):
        count = queryset.update(status='replied')
        self.message_user(request, f'{count} submissions marked as replied.')
    mark_as_replied.short_description = 'Mark selected submissions as replied'