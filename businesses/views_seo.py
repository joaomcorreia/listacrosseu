# businesses/views_seo.py
"""
SEO-Optimized Views for Maximum Search Engine Visibility
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Count
from .models import Business, Country, City, Category

def global_category_page(request, category):
    """Global category pages like /restaurants/ - High authority pages"""
    try:
        category_obj = Category.objects.get(slug=category)
    except Category.DoesNotExist:
        raise Http404("Category not found")
    
    businesses = Business.objects.filter(category=category_obj).select_related('city', 'city__country')
    
    # Get top countries for this category
    top_countries = (businesses.values('city__country__name', 'city__country__slug')
                    .annotate(business_count=Count('id'))
                    .order_by('-business_count')[:10])
    
    # Get top cities for this category
    top_cities = (businesses.values('city__name', 'city__slug', 'city__country__name', 'city__country__slug')
                 .annotate(business_count=Count('id'))
                 .order_by('-business_count')[:20])
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category_obj,
        'businesses': page_obj,
        'top_countries': top_countries,
        'top_cities': top_cities,
        'total_businesses': businesses.count(),
        'page_title': f'{category_obj.name} Businesses Across Europe - ListAcross.eu',
        'meta_description': f'Find the best {category_obj.name.lower()} businesses across all 27 EU countries. Browse {businesses.count()}+ verified {category_obj.name.lower()} listings on ListAcross.eu',
        'canonical_url': f'/{category}/',
    }
    
    return render(request, 'businesses/seo/global_category.html', context)

def category_country_businesses(request, category_slug, country_slug):
    """Category + Country pages like /restaurants/portugal/"""
    category = get_object_or_404(Category, slug=category_slug)
    country = get_object_or_404(Country, slug=country_slug)
    
    businesses = Business.objects.filter(
        category=category,
        city__country=country
    ).select_related('city')
    
    # Get top cities in this country for this category
    top_cities = (businesses.values('city__name', 'city__slug')
                 .annotate(business_count=Count('id'))
                 .order_by('-business_count')[:15])
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'country': country,
        'businesses': page_obj,
        'top_cities': top_cities,
        'total_businesses': businesses.count(),
        'page_title': f'{category.name} in {country.name} - European Business Directory',
        'meta_description': f'Discover {businesses.count()}+ {category.name.lower()} businesses in {country.name}. Complete directory with contact details, reviews and locations.',
        'canonical_url': f'/{category_slug}/{country_slug}/',
    }
    
    return render(request, 'businesses/seo/category_country.html', context)

def category_country_city_businesses(request, category_slug, country_slug, city_slug, page=1):
    """Category + Country + City pages like /restaurants/portugal/porto/"""
    category = get_object_or_404(Category, slug=category_slug)
    country = get_object_or_404(Country, slug=country_slug)
    city = get_object_or_404(City, slug=city_slug, country=country)
    
    businesses = Business.objects.filter(
        category=category,
        city=city
    ).select_related('city', 'city__country')
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page_obj = paginator.get_page(page)
    
    # Related categories in same city
    related_categories = (Business.objects.filter(city=city)
                         .exclude(category=category)
                         .values('category__name', 'category__slug')
                         .annotate(business_count=Count('id'))
                         .order_by('-business_count')[:8])
    
    context = {
        'category': category,
        'country': country,
        'city': city,
        'businesses': page_obj,
        'related_categories': related_categories,
        'total_businesses': businesses.count(),
        'page_title': f'Best {category.name} in {city.name}, {country.name} - ListAcross.eu',
        'meta_description': f'Find the top {category.name.lower()} businesses in {city.name}, {country.name}. {businesses.count()} verified listings with reviews, contact details and locations.',
        'canonical_url': f'/{category_slug}/{country_slug}/{city_slug}/',
    }
    
    return render(request, 'businesses/seo/category_country_city.html', context)

def country_category_businesses(request, country_slug, category_slug):
    """Enhanced country category pages like /portugal/restaurants/"""
    country = get_object_or_404(Country, slug=country_slug)
    category = get_object_or_404(Category, slug=category_slug)
    
    businesses = Business.objects.filter(
        city__country=country,
        category=category
    ).select_related('city')
    
    # Get top cities
    top_cities = (businesses.values('city__name', 'city__slug')
                 .annotate(business_count=Count('id'))
                 .order_by('-business_count')[:10])
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'country': country,
        'category': category,
        'businesses': page_obj,
        'top_cities': top_cities,
        'total_businesses': businesses.count(),
        'page_title': f'{category.name} Businesses in {country.name} - European Directory',
        'meta_description': f'Complete directory of {category.name.lower()} businesses in {country.name}. {businesses.count()}+ verified listings across major cities.',
        'canonical_url': f'/{country_slug}/{category_slug}/',
    }
    
    return render(request, 'businesses/seo/country_category.html', context)

def city_category_businesses(request, country_slug, city_slug, category_slug):
    """Enhanced city category pages like /portugal/porto/restaurants/"""
    country = get_object_or_404(Country, slug=country_slug)
    city = get_object_or_404(City, slug=city_slug, country=country)
    category = get_object_or_404(Category, slug=category_slug)
    
    businesses = Business.objects.filter(
        city=city,
        category=category
    ).select_related('category')
    
    # Pagination
    paginator = Paginator(businesses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Nearby cities with same category
    nearby_cities = (Business.objects.filter(
        city__country=country,
        category=category
    ).exclude(city=city)
    .values('city__name', 'city__slug')
    .annotate(business_count=Count('id'))
    .order_by('-business_count')[:8])
    
    context = {
        'country': country,
        'city': city,
        'category': category,
        'businesses': page_obj,
        'nearby_cities': nearby_cities,
        'total_businesses': businesses.count(),
        'page_title': f'Top {category.name} in {city.name}, {country.name} | ListAcross.eu',
        'meta_description': f'Discover the best {category.name.lower()} businesses in {city.name}, {country.name}. {businesses.count()} verified local businesses with reviews and contact information.',
        'canonical_url': f'/{country_slug}/{city_slug}/{category_slug}/',
    }
    
    return render(request, 'businesses/seo/city_category.html', context)

def business_detail_seo(request, country_slug, city_slug, category_slug, business_slug):
    """Enhanced business detail with full SEO path"""
    country = get_object_or_404(Country, slug=country_slug)
    city = get_object_or_404(City, slug=city_slug, country=country)
    category = get_object_or_404(Category, slug=category_slug)
    
    business = get_object_or_404(
        Business,
        slug=business_slug,
        city=city,
        category=category
    )
    
    # Related businesses in same category and city
    related_businesses = Business.objects.filter(
        city=city,
        category=category
    ).exclude(id=business.id)[:6]
    
    context = {
        'business': business,
        'country': country,
        'city': city,
        'category': category,
        'related_businesses': related_businesses,
        'page_title': f'{business.name} - {category.name} in {city.name}, {country.name}',
        'meta_description': f'{business.name} is a leading {category.name.lower()} business in {city.name}, {country.name}. Contact details, reviews, and business information.',
        'canonical_url': f'/{country_slug}/{city_slug}/{category_slug}/{business_slug}/',
    }
    
    return render(request, 'businesses/seo/business_detail_seo.html', context)

def top_restaurants_europe(request):
    """SEO landing page for top restaurants"""
    restaurants = Business.objects.filter(
        category__slug='restaurants'
    ).select_related('city', 'city__country')[:50]
    
    context = {
        'restaurants': restaurants,
        'page_title': 'Top Restaurants in Europe - European Dining Guide | ListAcross.eu',
        'meta_description': 'Discover Europe\'s finest restaurants across 27 countries. From Michelin stars to hidden gems, find the perfect dining experience.',
    }
    
    return render(request, 'businesses/seo/top_restaurants_europe.html', context)

def best_tech_companies_europe(request):
    """SEO landing page for top tech companies"""
    tech_companies = Business.objects.filter(
        category__slug='technology'
    ).select_related('city', 'city__country')[:50]
    
    context = {
        'tech_companies': tech_companies,
        'page_title': 'Best Technology Companies in Europe - European Tech Directory | ListAcross.eu',
        'meta_description': 'Explore Europe\'s leading technology companies. Connect with innovative startups and established tech firms across the EU.',
    }
    
    return render(request, 'businesses/seo/best_tech_companies_europe.html', context)

def european_business_directory(request):
    """Main SEO landing page"""
    # Get statistics
    total_businesses = Business.objects.count()
    total_countries = Country.objects.filter(is_active=True).count()
    total_cities = City.objects.count()
    
    # Top categories
    top_categories = (Business.objects.values('category__name', 'category__slug')
                     .annotate(business_count=Count('id'))
                     .order_by('-business_count')[:12])
    
    # Top countries
    top_countries = (Business.objects.values('city__country__name', 'city__country__slug')
                    .annotate(business_count=Count('id'))
                    .order_by('-business_count')[:15])
    
    context = {
        'total_businesses': total_businesses,
        'total_countries': total_countries,
        'total_cities': total_cities,
        'top_categories': top_categories,
        'top_countries': top_countries,
        'page_title': 'European Business Directory - Find Businesses Across 27 EU Countries | ListAcross.eu',
        'meta_description': f'Comprehensive European business directory with {total_businesses}+ verified businesses across {total_countries} EU countries. Find local businesses, read reviews, get contact details.',
    }
    
    return render(request, 'businesses/seo/european_business_directory.html', context)