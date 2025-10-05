from django.contrib import admin
from .models import Business, Category, Country, City, Review, BusinessImage
from .models_registration import BusinessRegistration, BusinessPhoto, BusinessClaim
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_eu_member', 'is_active']
    list_filter = ['is_eu_member', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'population', 'is_capital']
    list_filter = ['country', 'is_capital']
    search_fields = ['name', 'country__name']
    ordering = ['country__name', 'name']


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'owner', 'city', 'category', 'plan', 'status',
        'featured', 'verified', 'created_at'
    ]
    list_filter = [
        'plan', 'status', 'featured', 'verified', 'category',
        'city__country', 'created_at'
    ]
    search_fields = ['name', 'email', 'owner__email', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'views_count', 'clicks_count', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'slug', 'owner', 'description', 'short_description']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'website']
        }),
        ('Location', {
            'fields': ['address', 'city', 'postal_code', 'latitude', 'longitude']
        }),
        ('Categories', {
            'fields': ['category', 'subcategories']
        }),
        ('Media', {
            'fields': ['logo', 'cover_image']
        }),
        ('Business Hours', {
            'fields': [
                'monday_hours', 'tuesday_hours', 'wednesday_hours',
                'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours'
            ],
            'classes': ['collapse']
        }),
        ('Subscription & Status', {
            'fields': ['plan', 'status', 'featured', 'verified']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description', 'keywords'],
            'classes': ['collapse']
        }),
        ('Statistics', {
            'fields': ['views_count', 'clicks_count'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at', 'published_at', 'expires_at'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [BusinessImageInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'city', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'business', 'reviewer', 'rating', 'is_approved', 'created_at'
    ]
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['business__name', 'reviewer__email', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Review Information', {
            'fields': ['business', 'reviewer', 'rating', 'title', 'content']
        }),
        ('Moderation', {
            'fields': ['is_approved', 'moderation_notes']
        }),
        ('Business Response', {
            'fields': ['owner_response', 'response_date']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at']
        })
    ]


# Registration System Admin

@admin.register(BusinessRegistration)
class BusinessRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 'city', 'category', 'owner_name', 
        'verification_status', 'email_verified', 'premium_plan', 'created_at'
    ]
    list_filter = [
        'verification_status', 'email_verified', 'phone_verified', 
        'premium_plan', 'category', 'city__country', 'created_at'
    ]
    search_fields = ['business_name', 'owner_name', 'owner_email', 'email']
    readonly_fields = [
        'registration_id', 'email_verification_code', 'phone_verification_code',
        'created_at', 'updated_at'
    ]
    
    fieldsets = [
        ('Registration Status', {
            'fields': [
                'registration_id', 'verification_status', 'verification_notes',
                'email_verified', 'phone_verified', 'reviewed_by', 'reviewed_at'
            ]
        }),
        ('Business Information', {
            'fields': [
                'business_name', 'description', 'category', 'price_range'
            ]
        }),
        ('Location', {
            'fields': [
                'address', 'city', 'postal_code', 'latitude', 'longitude'
            ]
        }),
        ('Contact Information', {
            'fields': [
                'phone_number', 'email', 'website'
            ]
        }),
        ('Owner Information', {
            'fields': [
                'owner_name', 'owner_email', 'owner_phone'
            ]
        }),
        ('Premium Features', {
            'fields': [
                'wants_premium', 'premium_plan'
            ]
        }),
        ('Verification Codes', {
            'fields': [
                'email_verification_code', 'phone_verification_code'
            ],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': [
                'created_at', 'updated_at'
            ]
        })
    ]
    
    actions = ['approve_registrations', 'reject_registrations']
    
    def approve_registrations(self, request, queryset):
        approved_count = 0
        for registration in queryset.filter(verification_status='pending'):
            try:
                business = registration.approve_registration(request.user)
                approved_count += 1
                self.message_user(
                    request,
                    f'Successfully approved {registration.business_name} and created business listing.'
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Error approving {registration.business_name}: {str(e)}',
                    level='ERROR'
                )
        
        if approved_count > 0:
            self.message_user(
                request,
                f'Successfully approved {approved_count} business registrations.'
            )
    
    approve_registrations.short_description = "Approve selected registrations"
    
    def reject_registrations(self, request, queryset):
        updated = queryset.filter(verification_status='pending').update(
            verification_status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'Rejected {updated} registrations.')
    
    reject_registrations.short_description = "Reject selected registrations"


@admin.register(BusinessClaim)
class BusinessClaimAdmin(admin.ModelAdmin):
    list_display = [
        'business', 'claimant_name', 'claimant_email',
        'verification_method', 'status', 'created_at'
    ]
    list_filter = ['status', 'verification_method', 'created_at']
    search_fields = [
        'business__name', 'claimant_name', 'claimant_email'
    ]
    readonly_fields = ['created_at']
    
    fieldsets = [
        ('Claim Information', {
            'fields': [
                'business', 'claimant_name', 'claimant_email', 'claimant_phone'
            ]
        }),
        ('Verification', {
            'fields': [
                'ownership_proof', 'verification_method', 'status', 'notes'
            ]
        }),
        ('Review', {
            'fields': [
                'reviewed_by', 'reviewed_at'
            ]
        }),
        ('Timestamps', {
            'fields': ['created_at']
        })
    ]
    
    actions = ['approve_claims', 'reject_claims']
    
    def approve_claims(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'Approved {updated} business claims.')
    
    approve_claims.short_description = "Approve selected claims"
    
    def reject_claims(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'Rejected {updated} business claims.')
    
    reject_claims.short_description = "Reject selected claims"