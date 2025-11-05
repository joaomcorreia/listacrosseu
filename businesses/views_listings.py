"""
Business Listing Views
Views for browsing and searching businesses
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Business, Category, City, Country


def business_list(request):
    """List all businesses with filtering and pagination"""
    businesses = Business.objects.select_related('category', 'city', 'city__country').all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        businesses = businesses.filter(category=category)
    
    # Filter by city
    city_id = request.GET.get('city')
    if city_id:
        city = get_object_or_404(City, id=city_id)
        businesses = businesses.filter(city=city)
    
    # Filter by country
    country_code = request.GET.get('country')
    if country_code:
        country = get_object_or_404(Country, code=country_code)
        businesses = businesses.filter(city__country=country)
    
    # Search by name or description
    search = request.GET.get('search')
    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(businesses, 12)  # 12 businesses per page
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    # Get filter options
    categories = Category.objects.annotate(
        business_count=Count('businesses')
    ).filter(business_count__gt=0).order_by('name')
    
    countries = Country.objects.annotate(
        business_count=Count('cities__businesses')
    ).filter(business_count__gt=0).order_by('name')
    
    cities = City.objects.annotate(
        business_count=Count('businesses')
    ).filter(business_count__gt=0).order_by('name')
    
    context = {
        'businesses': businesses_page,
        'categories': categories,
        'countries': countries,
        'cities': cities,
        'current_category': category_slug,
        'current_city': city_id,
        'current_country': country_code,
        'current_search': search,
        'total_businesses': businesses.count(),
    }
    
    return render(request, 'businesses/business_list.html', context)


def business_detail(request, slug):
    """Display individual business details"""
    business = get_object_or_404(
        Business.objects.select_related('category', 'city', 'city__country'), 
        slug=slug
    )
    
    # Get related businesses in same city/category
    related_businesses = Business.objects.filter(
        Q(city=business.city) | Q(category=business.category)
    ).exclude(id=business.id)[:6]
    
    context = {
        'business': business,
        'related_businesses': related_businesses,
    }
    
    return render(request, 'businesses/business_detail.html', context)


def businesses_by_city(request, city_slug):
    """List all businesses in a specific city"""
    city = get_object_or_404(City, slug=city_slug)
    
    businesses = Business.objects.filter(city=city).select_related('category')
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        businesses = businesses.filter(category=category)
    
    # Search within city
    search = request.GET.get('search')
    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    # Get categories available in this city
    categories = Category.objects.annotate(
        business_count=Count('businesses')
    ).filter(
        businesses__city=city,
        business_count__gt=0
    ).order_by('name')
    
    context = {
        'city': city,
        'businesses': businesses_page,
        'categories': categories,
        'current_category': category_slug,
        'current_search': search,
        'total_businesses': businesses.count(),
    }
    
    return render(request, 'businesses/businesses_by_city.html', context)


def businesses_by_category(request, category_slug):
    """Redirect to SEO-optimized global category view"""
    from django.shortcuts import redirect
    from django.urls import reverse
    
    # Redirect to the SEO-optimized global category page
    return redirect(f'/{category_slug}/')


def city_list(request):
    """List all cities with business counts"""
    cities = City.objects.annotate(
        business_count=Count('businesses')
    ).filter(business_count__gt=0).select_related('country').order_by('-business_count')
    
    # Filter by country
    country_code = request.GET.get('country')
    if country_code:
        country = get_object_or_404(Country, code=country_code)
        cities = cities.filter(country=country)
    
    # Search cities
    search = request.GET.get('search')
    if search:
        cities = cities.filter(name__icontains=search)
    
    # Pagination
    paginator = Paginator(cities, 20)
    page = request.GET.get('page')
    cities_page = paginator.get_page(page)
    
    # Get countries with businesses
    countries = Country.objects.annotate(
        business_count=Count('cities__businesses')
    ).filter(business_count__gt=0).order_by('name')
    
    context = {
        'cities': cities_page,
        'countries': countries,
        'current_country': country_code,
        'current_search': search,
        'total_cities': cities.count(),
    }
    
    return render(request, 'businesses/city_list.html', context)