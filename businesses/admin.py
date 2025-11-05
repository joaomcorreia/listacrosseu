from django.contrib import admin
from .models import Business, Category, Country, City, Review, BusinessImage
from .models_registration import BusinessRegistration, BusinessPhoto, BusinessClaim
from .forms import BusinessForm, DuplicateCheckForm
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils import timezone
from django.template.response import TemplateResponse
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
import csv
import json
from datetime import datetime
from collections import defaultdict


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'business_count', 'countries_covered', 'is_active', 'sort_order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']
    
    def business_count(self, obj):
        """Count businesses in this category"""
        count = obj.businesses.count()
        if count > 0:
            url = f"/admin/businesses/business/?category__id__exact={obj.id}"
            return format_html(
                '<a href="{}" style="color: #007cba; font-weight: bold;">{} businesses</a>',
                url, count
            )
        return "0 businesses"
    business_count.short_description = "Businesses"
    
    def countries_covered(self, obj):
        """Count countries with businesses in this category"""
        countries_count = obj.businesses.values('city__country').distinct().count()
        if countries_count > 0:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{} countries</span>',
                countries_count
            )
        return "0 countries"
    countries_covered.short_description = "Countries"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'business_count', 'cities_count', 'is_eu_member', 'is_active']
    list_filter = ['is_eu_member', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    def business_count(self, obj):
        """Count businesses in this country"""
        count = Business.objects.filter(city__country=obj).count()
        if count > 0:
            url = f"/admin/businesses/business/?city__country__id__exact={obj.id}"
            return format_html(
                '<a href="{}" style="color: #007cba; font-weight: bold;">{} businesses</a>',
                url, count
            )
        return "0 businesses"
    business_count.short_description = "Businesses"
    
    def cities_count(self, obj):
        """Count cities with businesses in this country"""
        cities_with_businesses = obj.cities.filter(businesses__isnull=False).distinct().count()
        total_cities = obj.cities.count()
        if cities_with_businesses > 0:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{}</span> / {} cities',
                cities_with_businesses, total_cities
            )
        return f"0 / {total_cities} cities"
    cities_count.short_description = "Active Cities"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'business_count', 'categories_covered', 'population', 'is_capital']
    list_filter = ['country', 'is_capital']
    search_fields = ['name', 'country__name']
    ordering = ['country__name', 'name']
    
    def business_count(self, obj):
        """Count businesses in this city"""
        count = obj.businesses.count()
        if count > 0:
            url = f"/admin/businesses/business/?city__id__exact={obj.id}"
            return format_html(
                '<a href="{}" style="color: #007cba; font-weight: bold;">{} businesses</a>',
                url, count
            )
        return "0 businesses"
    business_count.short_description = "Businesses"
    
    def categories_covered(self, obj):
        """Count unique categories in this city"""
        categories_count = obj.businesses.values('category').distinct().count()
        if categories_count > 0:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{} categories</span>',
                categories_count
            )
        return "0 categories"
    categories_covered.short_description = "Categories"


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    form = BusinessForm
    list_display = [
        'name', 'city_with_country', 'category_name', 'plan_badge', 
        'status_badge', 'featured_badge', 'verified_badge', 'created_at'
    ]
    list_filter = [
        'plan', 'status', 'featured', 'verified', 'category',
        ('city__country', admin.RelatedOnlyFieldListFilter),
        'created_at'
    ]
    search_fields = ['name', 'email', 'owner__email', 'description', 'city__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'views_count', 'clicks_count', 'created_at', 'updated_at']
    actions = ['detect_duplicates_action', 'mark_as_verified', 'mark_as_unverified']
    change_list_template = 'admin/businesses/business/change_list.html'
    change_form_template = 'admin/businesses/business/change_form.html'
    
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
        return super().get_queryset(request).select_related('owner', 'city', 'category', 'city__country')
    
    def city_with_country(self, obj):
        """Display city with country"""
        if obj.city and obj.city.country:
            return f"{obj.city.name}, {obj.city.country.name}"
        return obj.city.name if obj.city else "No city"
    city_with_country.short_description = "Location"
    city_with_country.admin_order_field = 'city__name'
    
    def category_name(self, obj):
        """Display category name"""
        return obj.category.name if obj.category else "Uncategorized"
    category_name.short_description = "Category"
    category_name.admin_order_field = 'category__name'
    
    def plan_badge(self, obj):
        """Display plan as badge"""
        colors = {
            'free': '#6c757d',
            'basic': '#007bff', 
            'premium': '#28a745',
            'enterprise': '#dc3545'
        }
        color = colors.get(obj.plan, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.plan.title()
        )
    plan_badge.short_description = "Plan"
    plan_badge.admin_order_field = 'plan'
    
    def status_badge(self, obj):
        """Display status as badge"""
        colors = {
            'active': '#28a745',
            'inactive': '#6c757d',
            'pending': '#ffc107',
            'suspended': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.status.title()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'status'
    
    def featured_badge(self, obj):
        """Display featured status as badge"""
        if obj.featured:
            return format_html(
                '<span style="background: #ffc107; color: black; padding: 2px 6px; border-radius: 3px; font-size: 11px;">⭐ Featured</span>'
            )
        return format_html(
            '<span style="color: #6c757d; font-size: 11px;">-</span>'
        )
    featured_badge.short_description = "Featured"
    featured_badge.admin_order_field = 'featured'
    
    def verified_badge(self, obj):
        """Display verification status as badge"""
        if obj.verified:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">✓ Verified</span>'
            )
        return format_html(
            '<span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">Unverified</span>'
        )
    verified_badge.short_description = "Verified"
    verified_badge.admin_order_field = 'verified'
    
    def detect_duplicates_action(self, request, queryset):
        """Custom action to detect duplicates for selected businesses"""
        duplicate_count = 0
        business_names = []
        
        for business in queryset:
            # Find potential duplicates for this business
            duplicates = Business.objects.filter(
                name=business.name,
                city=business.city
            ).exclude(id=business.id)
            
            if duplicates.exists():
                duplicate_count += duplicates.count()
                business_names.append(business.name)
        
        if duplicate_count > 0:
            self.message_user(
                request,
                format_html(
                    'Found {} potential duplicates for {} businesses. '
                    '<a href="/admin/duplicate-detection/" style="color: #007bff; text-decoration: underline;">'
                    'Go to Duplicate Detection</a> for detailed analysis.',
                    duplicate_count, len(business_names)
                ),
                level=messages.WARNING
            )
        else:
            self.message_user(request, "No duplicates found for selected businesses.", level=messages.SUCCESS)
    
    detect_duplicates_action.short_description = "🔍 Check for duplicates"
    
    def mark_as_verified(self, request, queryset):
        """Mark selected businesses as verified"""
        updated = queryset.update(verified=True)
        self.message_user(request, f"{updated} businesses marked as verified.", level=messages.SUCCESS)
    
    mark_as_verified.short_description = "✓ Mark as verified"
    
    def mark_as_unverified(self, request, queryset):
        """Mark selected businesses as unverified"""
        updated = queryset.update(verified=False)
        self.message_user(request, f"{updated} businesses marked as unverified.", level=messages.SUCCESS)
    
    mark_as_unverified.short_description = "✗ Mark as unverified"


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


# Custom Admin Site with Dashboard
class BusinessDirectoryAdminSite(admin.AdminSite):
    site_header = "List Across EU - Business Directory Admin"
    site_title = "List Across EU Admin"
    index_title = "Business Directory Management Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('business-stats/', self.admin_view(self.business_stats_view), name='business_stats'),
            path('export-data/', self.admin_view(self.export_data_view), name='export_data'),
            path('duplicate-detection/', self.admin_view(self.duplicate_detection_view), name='duplicate_detection'),
            path('duplicate-cleanup/', self.admin_view(self.duplicate_cleanup_view), name='duplicate_cleanup'),
            path('duplicate-check-ajax/', self.admin_view(self.duplicate_check_ajax), name='duplicate_check_ajax'),
        ]
        return custom_urls + urls
    
    def business_stats_view(self, request):
        """Custom dashboard view showing comprehensive business statistics"""
        
        # Overall stats
        total_businesses = Business.objects.count()
        total_countries = Country.objects.count()
        total_cities = City.objects.count()
        total_categories = Category.objects.count()
        
        # Active stats (with businesses)
        countries_with_businesses = Country.objects.filter(cities__businesses__isnull=False).distinct().count()
        cities_with_businesses = City.objects.filter(businesses__isnull=False).count()
        categories_with_businesses = Category.objects.filter(businesses__isnull=False).count()
        
        # Top countries by business count
        top_countries = Country.objects.annotate(
            business_count=Count('cities__businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:10]
        
        # Top cities by business count
        top_cities = City.objects.annotate(
            business_count=Count('businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:15]
        
        # Top categories by business count
        top_categories = Category.objects.annotate(
            business_count=Count('businesses')
        ).filter(business_count__gt=0).order_by('-business_count')[:15]
        
        # Empty categories (need attention)
        empty_categories = Category.objects.filter(businesses__isnull=True).order_by('name')
        
        # Empty countries (need attention)
        empty_countries = Country.objects.filter(cities__businesses__isnull=True).distinct().order_by('name')
        
        context = {
            'title': 'Business Statistics Dashboard',
            'total_businesses': total_businesses,
            'total_countries': total_countries,
            'total_cities': total_cities,
            'total_categories': total_categories,
            'countries_with_businesses': countries_with_businesses,
            'cities_with_businesses': cities_with_businesses,
            'categories_with_businesses': categories_with_businesses,
            'top_countries': top_countries,
            'top_cities': top_cities,
            'top_categories': top_categories,
            'empty_categories': empty_categories,
            'empty_countries': empty_countries,
            'coverage_percentage': {
                'countries': round((countries_with_businesses / total_countries) * 100, 1) if total_countries > 0 else 0,
                'cities': round((cities_with_businesses / total_cities) * 100, 1) if total_cities > 0 else 0,
                'categories': round((categories_with_businesses / total_categories) * 100, 1) if total_categories > 0 else 0,
            }
        }
        
        return TemplateResponse(request, 'admin/business_stats.html', context)

    def duplicate_detection_view(self, request):
        """Detect and display ALL duplicate businesses for manual confirmation"""
        
        # Get filter parameters
        country_filter = request.GET.get('country', '')
        city_filter = request.GET.get('city', '')
        threshold = int(request.GET.get('threshold', 2))
        show_type = request.GET.get('show_type', 'summary')  # summary, exact, name, address
        
        # Build base query
        base_query = Business.objects.select_related('city__country', 'category', 'owner')
        if country_filter:
            base_query = base_query.filter(city__country__code__iexact=country_filter)
        if city_filter:
            base_query = base_query.filter(city__name__icontains=city_filter)
        
        # Find exact duplicates (same name, city, address)
        exact_duplicates = base_query.values(
            'name', 'city', 'address'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        # Find name duplicates in same city
        name_duplicates = base_query.values(
            'name', 'city'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        # Find potential address duplicates
        address_duplicates = base_query.exclude(
            Q(address__isnull=True) | Q(address='')
        ).values(
            'address', 'city'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=threshold).order_by('-count')
        
        # Get detailed groups based on what user wants to see
        detailed_groups = []
        
        if show_type == 'exact' or show_type == 'summary':
            # Get ALL exact duplicate groups
            for dup in exact_duplicates:
                try:
                    city = City.objects.get(id=dup['city'])
                    businesses = base_query.filter(
                        name=dup['name'],
                        city=city,
                        address=dup['address']
                    ).order_by('created_at')
                    
                    if businesses.count() >= threshold:
                        detailed_groups.append({
                            'type': 'exact',
                            'title': f"Exact Match: {dup['name']} in {city.name}",
                            'description': f"Same name, city, and address: {dup['address'][:100]}...",
                            'count': dup['count'],
                            'businesses': businesses,
                            'suggested_keep': businesses.first(),  # Keep oldest
                            'suggested_remove': businesses[1:],   # Remove newer ones
                        })
                except City.DoesNotExist:
                    continue
        
        if show_type == 'name' or show_type == 'summary':
            # Get ALL name duplicate groups (excluding exact matches)
            exact_pairs = set()
            for dup in exact_duplicates:
                exact_pairs.add((dup['name'], dup['city']))
            
            for dup in name_duplicates:
                # Skip if this is already covered by exact duplicates
                if (dup['name'], dup['city']) in exact_pairs:
                    continue
                
                try:
                    city = City.objects.get(id=dup['city'])
                    businesses = base_query.filter(
                        name=dup['name'],
                        city=city
                    ).order_by('created_at')
                    
                    if businesses.count() >= threshold:
                        # Check if these have different addresses (legitimate different locations)
                        addresses = businesses.values_list('address', flat=True).distinct()
                        
                        detailed_groups.append({
                            'type': 'name',
                            'title': f"Same Name: {dup['name']} in {city.name}",
                            'description': f"Same business name, {len(addresses)} different addresses",
                            'count': dup['count'],
                            'businesses': businesses,
                            'suggested_keep': None,  # Requires manual review
                            'suggested_remove': [],
                            'addresses': list(addresses),
                            'needs_manual_review': True,
                        })
                except City.DoesNotExist:
                    continue
        
        if show_type == 'address' or show_type == 'summary':
            # Get ALL address duplicate groups (excluding exact matches)
            exact_address_pairs = set()
            for dup in exact_duplicates:
                exact_address_pairs.add((dup['address'], dup['city']))
            
            for dup in address_duplicates:
                # Skip if this is already covered by exact duplicates
                if (dup['address'], dup['city']) in exact_address_pairs:
                    continue
                
                try:
                    city = City.objects.get(id=dup['city'])
                    businesses = base_query.filter(
                        address=dup['address'],
                        city=city
                    ).order_by('created_at')
                    
                    if businesses.count() >= threshold:
                        # SMART ADDRESS DUPLICATE DETECTION
                        business_names = businesses.values_list('name', flat=True).distinct()
                        categories = businesses.values_list('category__name', flat=True).distinct()
                        
                        # Only flag as duplicates if businesses have SIMILAR names or categories
                        # Different businesses at same address (shopping malls, etc.) are legitimate
                        suspicious_pairs = []
                        business_list = list(businesses)
                        
                        for i, business1 in enumerate(business_list):
                            for business2 in business_list[i+1:]:
                                # Check for similar names (fuzzy matching)
                                name1_normalized = Business.normalize_business_name(business1.name)
                                name2_normalized = Business.normalize_business_name(business2.name)
                                
                                # Flag as suspicious if:
                                # 1. Very similar normalized names (likely duplicates)
                                # 2. Same category and similar names
                                # 3. Empty/generic names that could be duplicates
                                is_suspicious = False
                                
                                # Similar names check
                                if (len(name1_normalized) > 3 and len(name2_normalized) > 3):
                                    similarity_ratio = len(set(name1_normalized.split()) & set(name2_normalized.split())) / max(len(name1_normalized.split()), len(name2_normalized.split()))
                                    if similarity_ratio > 0.6:  # 60% word similarity
                                        is_suspicious = True
                                
                                # Same category + some name similarity
                                if business1.category == business2.category and business1.category:
                                    if similarity_ratio > 0.3:  # Lower threshold for same category
                                        is_suspicious = True
                                
                                # Generic or empty names
                                if (len(name1_normalized) <= 3 or len(name2_normalized) <= 3 or
                                    name1_normalized in ['business', 'shop', 'store', 'company'] or
                                    name2_normalized in ['business', 'shop', 'store', 'company']):
                                    is_suspicious = True
                                
                                if is_suspicious and (business1.id, business2.id) not in [(p[1].id, p[0].id) for p in suspicious_pairs]:
                                    suspicious_pairs.append((business1, business2))
                        
                        # Only add to duplicate groups if we found suspicious pairs
                        if suspicious_pairs:
                            detailed_groups.append({
                                'type': 'address',
                                'title': f"Suspicious Address Duplicates: {dup['address'][:50]}... in {city.name}",
                                'description': f"Same address with {len(suspicious_pairs)} potentially duplicate business pairs. Review carefully - different businesses at same location are legitimate.",
                                'count': len(suspicious_pairs) * 2,  # Approximate count
                                'businesses': businesses,
                                'suggested_keep': None,  # Requires manual review
                                'suggested_remove': [],
                                'business_names': list(business_names),
                                'needs_manual_review': True,
                                'suspicious_pairs': suspicious_pairs,
                                'warning': 'Multiple businesses at same address can be legitimate (shopping malls, office buildings, etc.)'
                            })
                except City.DoesNotExist:
                    continue
        
        # Limit display for performance (show top 50 groups)
        if show_type == 'summary':
            detailed_groups = detailed_groups[:20]  # Summary shows top 20
        else:
            detailed_groups = detailed_groups[:100]  # Individual views show more
        
        # Get countries and cities for filters
        countries = Country.objects.filter(
            cities__businesses__isnull=False
        ).distinct().order_by('name')
        
        cities = City.objects.filter(
            businesses__isnull=False
        ).order_by('name')
        
        context = {
            'title': 'Duplicate Detection & Manual Confirmation',
            'exact_count': exact_duplicates.count(),
            'name_count': name_duplicates.count(), 
            'address_count': address_duplicates.count(),
            'exact_groups': exact_duplicates.count(),
            'name_groups': name_duplicates.count(),
            'address_groups': address_duplicates.count(),
            'detailed_groups': detailed_groups,
            'show_type': show_type,
            'countries': countries,
            'cities': cities,
            'current_country': country_filter,
            'current_city': city_filter,
            'current_threshold': threshold,
            'has_duplicates': len(detailed_groups) > 0,
        }
        
        return TemplateResponse(request, 'admin/duplicate_detection.html', context)
    
    def duplicate_cleanup_view(self, request):
        """Handle bulk duplicate cleanup"""
        
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'cleanup_selected':
                # Get selected business IDs to remove
                remove_ids = request.POST.getlist('remove_ids')
                
                if remove_ids:
                    try:
                        # Convert to proper format and remove duplicates
                        remove_ids = [str(id).strip() for id in remove_ids if id.strip()]
                        businesses_to_remove = Business.objects.filter(id__in=remove_ids)
                        count = businesses_to_remove.count()
                        
                        # Delete the businesses
                        businesses_to_remove.delete()
                        
                        messages.success(
                            request, 
                            f'Successfully removed {count} duplicate businesses.'
                        )
                    except Exception as e:
                        messages.error(
                            request,
                            f'Error removing duplicates: {str(e)}'
                        )
                else:
                    messages.warning(request, 'No businesses selected for removal.')
            
            elif action == 'cleanup_all_exact':
                # Automatically cleanup all exact duplicates
                try:
                    exact_duplicates = Business.objects.values(
                        'name', 'city', 'address'
                    ).annotate(
                        count=Count('id')
                    ).filter(count__gt=1)
                    
                    total_removed = 0
                    for dup in exact_duplicates:
                        businesses = Business.objects.filter(
                            name=dup['name'],
                            city_id=dup['city'],
                            address=dup['address']
                        ).order_by('created_at')
                        
                        if businesses.count() > 1:
                            # Keep the first, remove the rest
                            to_remove = businesses[1:]
                            removed_count = to_remove.count()
                            to_remove.delete()
                            total_removed += removed_count
                    
                    messages.success(
                        request,
                        f'Successfully removed {total_removed} duplicate businesses automatically.'
                    )
                except Exception as e:
                    messages.error(
                        request,
                        f'Error during automatic cleanup: {str(e)}'
                    )
        
        # Redirect back to duplicate detection
        return redirect('admin:duplicate_detection')

    def export_data_view(self, request):
        """Export business data as CSV"""
        
        export_type = request.GET.get('type', 'summary')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_type == 'all':
            # Export all businesses
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="all_businesses_{timestamp}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Name', 'Category', 'Country', 'City', 'Address', 'Phone', 'Email', 'Website', 'Verified', 'Status'])
            
            businesses = Business.objects.select_related('category', 'city__country').order_by('city__country__name', 'city__name', 'name')
            for business in businesses:
                writer.writerow([
                    business.name,
                    business.category.name if business.category else 'Uncategorized',
                    business.city.country.name if business.city else '',
                    business.city.name if business.city else '',
                    business.address or '',
                    business.phone or '',
                    business.email or '',
                    business.website or '',
                    'Yes' if business.verified else 'No',
                    business.status.title()
                ])
            
            return response
        
        elif export_type == 'summary':
            # Export summary statistics
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="business_summary_{timestamp}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Metric', 'Count', 'Percentage'])
            
            total = Business.objects.count()
            writer.writerow(['Total Businesses', total, '100%'])
            writer.writerow(['', '', ''])
            
            # By country
            writer.writerow(['BY COUNTRY', '', ''])
            countries = Business.objects.select_related('city__country').values(
                'city__country__name'
            ).annotate(count=Count('id')).order_by('-count')
            
            for country in countries:
                percentage = f"{(country['count']/total*100):.1f}%"
                writer.writerow([country['city__country__name'], country['count'], percentage])
            
            writer.writerow(['', '', ''])
            
            # By city (top 15)
            writer.writerow(['TOP CITIES', '', ''])
            cities = Business.objects.values('city__name', 'city__country__name').annotate(
                count=Count('id')
            ).order_by('-count')[:15]
            
            for city in cities:
                city_name = f"{city['city__name']}, {city['city__country__name']}"
                percentage = f"{(city['count']/total*100):.1f}%"
                writer.writerow([city_name, city['count'], percentage])
            
            return response
        
        elif export_type in ['germany', 'spain', 'france']:
            # Export specific country
            country = Country.objects.get(slug=export_type)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="businesses_{export_type}_{timestamp}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Name', 'Category', 'City', 'Address', 'Phone', 'Email', 'Website', 'Verified'])
            
            businesses = Business.objects.filter(city__country=country).select_related('category', 'city').order_by('city__name', 'name')
            for business in businesses:
                writer.writerow([
                    business.name,
                    business.category.name if business.category else 'Uncategorized',
                    business.city.name,
                    business.address or '',
                    business.phone or '',
                    business.email or '',
                    business.website or '',
                    'Yes' if business.verified else 'No'
                ])
            
            return response
        
        else:
            # Show export options page
            context = {
                'title': 'Export Business Data',
                'total_businesses': Business.objects.count(),
                'countries': Country.objects.filter(cities__businesses__isnull=False).distinct().annotate(
                    business_count=Count('cities__businesses')
                ).order_by('-business_count')
            }
            return TemplateResponse(request, 'admin/export_data.html', context)

    def index(self, request, extra_context=None):
        """Enhanced admin index with quick stats"""
        extra_context = extra_context or {}
        
        # Count duplicates for quick stats
        exact_duplicates = Business.objects.values(
            'name', 'city', 'address'
        ).annotate(
            count=Count('id')
        ).filter(count__gt=1).count()
        
        # Add quick stats to the main admin page
        extra_context.update({
            'total_businesses': Business.objects.count(),
            'countries_with_businesses': Country.objects.filter(cities__businesses__isnull=False).distinct().count(),
            'cities_with_businesses': City.objects.filter(businesses__isnull=False).count(),
            'categories_with_businesses': Category.objects.filter(businesses__isnull=False).count(),
            'duplicate_groups': exact_duplicates,
        })
        
        return super().index(request, extra_context)
    
    def duplicate_check_ajax(self, request):
        """AJAX endpoint for real-time duplicate checking"""
        if request.method != 'POST':
            return JsonResponse({'error': 'Only POST requests allowed'})
            
        form = DuplicateCheckForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'error': 'Invalid form data'})
            
        result = form.check_duplicates()
        return JsonResponse(result)

# Create custom admin site instance
admin_site = BusinessDirectoryAdminSite(name='businessadmin')

# Register all models with the custom admin site
admin_site.register(Category, CategoryAdmin)
admin_site.register(Country, CountryAdmin)
admin_site.register(City, CityAdmin)
admin_site.register(Business, BusinessAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(BusinessImage)  # Use default admin for BusinessImage
admin_site.register(BusinessRegistration, BusinessRegistrationAdmin)
admin_site.register(BusinessClaim, BusinessClaimAdmin)

# Also register BusinessPhoto if it exists
try:
    from .models_registration import BusinessPhoto
    admin_site.register(BusinessPhoto)  # Use default admin
except ImportError:
    pass