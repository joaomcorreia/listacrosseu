# businesses/views_country_city.py
"""
Views for enhanced country/city URL structure
URLs like: /portugal/ and /portugal/porto/
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Country, City, Business, Category


def country_businesses(request, country_slug):
    """
    Show all businesses in a country
    URL: /portugal/
    """
    country = get_object_or_404(Country, slug=country_slug, is_active=True)
    
    # Get all businesses in this country
    businesses = Business.objects.filter(
        city__country=country,
        verified=True
    ).select_related('city', 'category').order_by('name')
    
    # Get categories with business counts for this country
    categories = Category.objects.filter(
        businesses__city__country=country,
        businesses__verified=True
    ).annotate(
        business_count=Count('businesses')
    ).order_by('-business_count')[:10]
    
    # Get cities with business counts for this country
    cities = City.objects.filter(
        country=country,
        businesses__verified=True
    ).annotate(
        business_count=Count('businesses')
    ).order_by('-business_count')
    
    # Get top 3 categories for each city for enhanced display
    cities_with_categories = []
    for city in cities:
        city_categories = Category.objects.filter(
            businesses__city=city,
            businesses__verified=True
        ).annotate(
            business_count=Count('businesses')
        ).order_by('-business_count')[:3]
        
        cities_with_categories.append({
            'city': city,
            'categories': city_categories
        })
    
    # Pagination
    paginator = Paginator(businesses, 24)  # Show 24 businesses per page
    page_number = request.GET.get('page')
    businesses_page = paginator.get_page(page_number)
    
    # Apply category filter if specified
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            businesses = businesses.filter(category=category)
            businesses_page = Paginator(businesses, 24).get_page(page_number)
        except Category.DoesNotExist:
            pass
    
    context = {
        'country': country,
        'businesses': businesses_page,
        'cities': cities,
        'cities_with_categories': cities_with_categories,
        'categories': categories,
        'total_businesses': businesses.count(),
        'location_type': 'country',
        'location_code': country.code,
        'page_title': f'{country.name} Business Directory',
        'meta_description': f'Discover businesses in {country.name}. Browse {businesses.count()} verified companies across {cities.count()} cities.',
    }
    
    return render(request, 'businesses/country_detail.html', context)


def city_businesses(request, country_slug, city_slug):
    """
    Show all businesses in a specific city
    URL: /portugal/porto/
    """
    country = get_object_or_404(Country, slug=country_slug, is_active=True)
    city = get_object_or_404(City, slug=city_slug, country=country)
    
    # Get all businesses in this city
    businesses = Business.objects.filter(
        city=city,
        verified=True
    ).select_related('category').order_by('name')
    
    # Apply category filter if specified in query parameters
    category_slug = request.GET.get('category')
    filtered_category = None
    if category_slug:
        try:
            filtered_category = Category.objects.get(slug=category_slug)
            businesses = businesses.filter(category=filtered_category)
        except Category.DoesNotExist:
            # If category doesn't exist, raise 404
            raise get_object_or_404(Category, slug=category_slug)
    
    # Get all main categories with business counts for this city
    main_category_names = [
        'Restaurant', 'Technology', 'Tourism', 'Retail', 'Health', 'Education',
        'Finance', 'Real Estate', 'Services', 'Manufacturing', 'Construction', 'Transportation'
    ]
    
    # Define subcategories for each main category
    category_subcategories = {
        'Restaurant': ['Fine Dining', 'Fast Food', 'Cafés & Coffee', 'Bars & Pubs'],
        'Technology': ['Software Development', 'IT Services', 'Web Development', 'Cybersecurity'],
        'Tourism': ['Hotels', 'Tour Operators', 'Travel Agencies', 'Tourist Attractions'],
        'Retail': ['Clothing Stores', 'Electronics', 'Supermarkets', 'Shopping'],
        'Health': ['Medical Centers', 'Pharmacies', 'Dental Clinics', 'Physiotherapy'],
        'Education': ['Schools', 'Universities', 'Training Centers', 'Language Schools'],
        'Finance': ['Banks', 'Insurance', 'Investment Banks', 'Financial Planning'],
        'Real Estate': ['Real Estate Agencies', 'Property Management', 'Construction', 'Interior Design'],
        'Services': ['Legal Services', 'Consulting', 'Marketing Agencies', 'Business Services'],
        'Manufacturing': ['Food Processing', 'Automotive Manufacturing', 'Electronics Manufacturing', 'Textile Manufacturing'],
        'Construction': ['Building Construction', 'Engineering', 'Architecture', 'Home Renovation'],
        'Transportation': ['Logistics Companies', 'Car Rental', 'Public Transport', 'Moving Services']
    }

    categories_with_counts = []
    for cat_name in main_category_names:
        try:
            category = Category.objects.get(name=cat_name)
            business_count = businesses.filter(category=category).count()
            
            # Get subcategories and their business counts
            subcategories_data = []
            if cat_name in category_subcategories:
                for subcat_name in category_subcategories[cat_name]:
                    try:
                        subcategory = Category.objects.get(name=subcat_name)
                        subcat_business_count = businesses.filter(category=subcategory).count()
                        subcategories_data.append({
                            'name': subcat_name,
                            'slug': subcategory.slug,
                            'business_count': subcat_business_count
                        })
                    except Category.DoesNotExist:
                        # If subcategory doesn't exist, add it with 0 count
                        subcategories_data.append({
                            'name': subcat_name,
                            'slug': subcat_name.lower().replace(' ', '-').replace('&', ''),
                            'business_count': 0
                        })
            
            categories_with_counts.append({
                'category': category,
                'business_count': business_count,
                'subcategories': subcategories_data
            })
        except Category.DoesNotExist:
            continue
    
    # Sort by business count descending
    categories_with_counts.sort(key=lambda x: x['business_count'], reverse=True)
    
    # Pagination
    paginator = Paginator(businesses, 24)
    page_number = request.GET.get('page')
    businesses_page = paginator.get_page(page_number)
    
    # Update page title and description based on category filter
    if filtered_category:
        page_title = f'{filtered_category.name} in {city.name}, {country.name} - Business Directory'
        meta_description = f'Find {filtered_category.name.lower()} businesses in {city.name}, {country.name}. Browse {businesses.count()} verified {filtered_category.name.lower()} companies.'
    else:
        page_title = f'{city.name}, {country.name} Business Directory'
        meta_description = f'Discover businesses in {city.name}, {country.name}. Browse {businesses.count()} verified local companies.'
    
    context = {
        'country': country,
        'city': city,
        'businesses': businesses_page,
        'categories': categories_with_counts,
        'filtered_category': filtered_category,
        'total_businesses': businesses.count(),
        'location_type': 'city',
        'location_code': city.name.lower(),
        'page_title': page_title,
        'meta_description': meta_description,
    }
    
    return render(request, 'businesses/city_detail.html', context)


def country_list(request):
    """
    List all countries with business counts
    URL: /countries/
    """
    countries = Country.objects.filter(
        is_active=True,
        cities__businesses__verified=True
    ).annotate(
        business_count=Count('cities__businesses', distinct=True),
        city_count=Count('cities', distinct=True)
    ).order_by('name')
    
    context = {
        'countries': countries,
        'total_countries': countries.count(),
        'page_title': 'European Countries - Business Directory',
        'meta_description': 'Browse businesses by country across Europe. Find verified companies in all 27 EU member states.',
    }
    
    return render(request, 'businesses/country_list.html', context)