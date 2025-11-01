from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from catalog.models import Category, Business
from geo.models import Country, City, Town
from counters.models import CategoryCountry, CategoryCountryCity, CategoryCityTown
from .serializers import (
    CategorySerializer, CountrySerializer, CitySerializer, TownSerializer,
    BusinessSerializer, UniformResponseSerializer
)


def build_breadcrumbs(level, lang, category_slug=None, country_code=None, city_slug=None, town_slug=None):
    """Build breadcrumb navigation"""
    breadcrumbs = [{'label': 'Categories', 'href': f'/{lang}/categories'}]
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            breadcrumbs.append({
                'label': category.get_name(lang),
                'href': f'/{lang}/categories/{category_slug}'
            })
        except Category.DoesNotExist:
            pass
    
    if country_code:
        try:
            country = Country.objects.get(code=country_code)
            breadcrumbs.append({
                'label': country.get_name(lang),
                'href': f'/{lang}/{country_code}/{category_slug}' if category_slug else f'/{lang}/{country_code}'
            })
        except Country.DoesNotExist:
            pass
    
    if city_slug:
        try:
            city = City.objects.get(slug=city_slug, country__code=country_code)
            breadcrumbs.append({
                'label': city.name,
                'href': f'/{lang}/{country_code}/{city_slug}/{category_slug}' if category_slug else f'/{lang}/{country_code}/{city_slug}'
            })
        except City.DoesNotExist:
            pass
    
    if town_slug:
        try:
            town = Town.objects.get(slug=town_slug, city__slug=city_slug, city__country__code=country_code)
            breadcrumbs.append({
                'label': town.name,
                'href': f'/{lang}/{country_code}/{city_slug}/{town_slug}/{category_slug}' if category_slug else f'/{lang}/{country_code}/{city_slug}/{town_slug}'
            })
        except Town.DoesNotExist:
            pass
    
    return breadcrumbs


@api_view(['GET'])
def categories_list(request):
    """GET /api/categories - List all categories with global or country-specific counts"""
    lang = request.GET.get('lang', 'en')
    country_code = request.GET.get('country')
    
    # Get categories with business counts
    categories = Category.objects.filter(is_active=True)
    
    if country_code:
        # Filter by specific country
        try:
            country = Country.objects.get(code=country_code)
            category_counts = CategoryCountry.objects.filter(country=country).values('category', 'business_count')
            count_dict = {item['category']: item['business_count'] for item in category_counts}
        except Country.DoesNotExist:
            count_dict = {}
    else:
        # Global counts
        category_counts = CategoryCountry.objects.values('category').annotate(
            total_count=Sum('business_count')
        ).values_list('category', 'total_count')
        count_dict = dict(category_counts)
    
    # Prepare category data
    category_data = []
    for category in categories:
        count = count_dict.get(category.id, 0)
        if count > 0:  # Only show categories with businesses
            category_data.append({
                'slug': category.slug,
                'name': category.get_name(lang),
                'count': count
            })
    
    response_data = {
        'level': 'categories',
        'breadcrumbs': build_breadcrumbs('categories', lang),
        'facets': {},
        'items': category_data,
        'pagination': {'page': 1, 'page_size': len(category_data), 'has_more': False}
    }
    
    return Response(response_data)


@api_view(['GET'])
def category_countries(request, category_slug):
    """GET /api/categories/{categorySlug}/countries - Countries with count > 0 for category"""
    lang = request.GET.get('lang', 'en')
    
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    
    # Get countries with business counts for this category
    country_counts = CategoryCountry.objects.filter(
        category=category,
        business_count__gt=0
    ).select_related('country')
    
    countries_data = []
    for cc in country_counts:
        countries_data.append({
            'code': cc.country.code,
            'name': cc.country.get_name(lang),
            'count': cc.business_count
        })
    
    response_data = {
        'level': 'category',
        'breadcrumbs': build_breadcrumbs('category', lang, category_slug=category_slug),
        'facets': {'countries': countries_data},
        'items': countries_data,
        'pagination': {'page': 1, 'page_size': len(countries_data), 'has_more': False}
    }
    
    return Response(response_data)


@api_view(['GET'])
def category_country_cities(request, category_slug, country_code):
    """GET /api/categories/{categorySlug}/countries/{countryCode}/cities"""
    lang = request.GET.get('lang', 'en')
    
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    country = get_object_or_404(Country, code=country_code, is_active=True)
    
    # Get cities with business counts
    city_counts = CategoryCountryCity.objects.filter(
        category=category,
        country=country,
        business_count__gt=0
    ).select_related('city')
    
    cities_data = []
    for ccc in city_counts:
        cities_data.append({
            'slug': ccc.city.slug,
            'name': ccc.city.name,
            'count': ccc.business_count
        })
    
    response_data = {
        'level': 'country',
        'breadcrumbs': build_breadcrumbs('country', lang, category_slug=category_slug, country_code=country_code),
        'facets': {'cities': cities_data},
        'items': cities_data,
        'pagination': {'page': 1, 'page_size': len(cities_data), 'has_more': False}
    }
    
    return Response(response_data)


@api_view(['GET'])
def category_city_towns(request, category_slug, country_code, city_slug):
    """GET /api/categories/{categorySlug}/countries/{countryCode}/cities/{citySlug}/towns"""
    lang = request.GET.get('lang', 'en')
    
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    country = get_object_or_404(Country, code=country_code, is_active=True)
    city = get_object_or_404(City, slug=city_slug, country=country, is_active=True)
    
    # Get towns with business counts
    town_counts = CategoryCityTown.objects.filter(
        category=category,
        city=city,
        business_count__gt=0
    ).select_related('town')
    
    towns_data = []
    for cct in town_counts:
        towns_data.append({
            'slug': cct.town.slug,
            'name': cct.town.name,
            'count': cct.business_count
        })
    
    response_data = {
        'level': 'city',
        'breadcrumbs': build_breadcrumbs('city', lang, category_slug=category_slug, country_code=country_code, city_slug=city_slug),
        'facets': {'towns': towns_data},
        'items': towns_data,
        'pagination': {'page': 1, 'page_size': len(towns_data), 'has_more': False}
    }
    
    return Response(response_data)


@api_view(['GET'])
def search(request):
    """GET /api/search - Search businesses with faceted navigation"""
    lang = request.GET.get('lang', 'en')
    category_slug = request.GET.get('category', '')
    country_code = request.GET.get('country', '')
    city_slug = request.GET.get('city', '')
    town_slug = request.GET.get('town', '')
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 24))
    
    # Build query filters
    filters = Q(status='active')
    
    category = None
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
            filters &= Q(categories=category)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if country_code:
        try:
            country = Country.objects.get(code=country_code, is_active=True)
            filters &= Q(country=country)
        except Country.DoesNotExist:
            return Response({'error': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if city_slug:
        try:
            city = City.objects.get(slug=city_slug, country__code=country_code, is_active=True)
            filters &= Q(city=city)
        except City.DoesNotExist:
            return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if town_slug:
        try:
            town = Town.objects.get(slug=town_slug, city__slug=city_slug, city__country__code=country_code, is_active=True)
            filters &= Q(town=town)
        except Town.DoesNotExist:
            return Response({'error': 'Town not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if q:
        filters &= Q(name__icontains=q)
    
    # Get businesses
    businesses = Business.objects.filter(filters).select_related('city', 'town', 'country')
    
    # Paginate results
    paginator = Paginator(businesses, page_size)
    page_obj = paginator.get_page(page)
    
    # Serialize business data
    business_serializer = BusinessSerializer(page_obj.object_list, many=True)
    
    # Build facets (simplified - you might want to optimize this)
    facets = {}
    
    # Determine level for breadcrumbs
    if town_slug:
        level = 'town'
    elif city_slug:
        level = 'city'
    elif country_code:
        level = 'country'
    elif category_slug:
        level = 'category'
    else:
        level = 'results'
    
    response_data = {
        'level': level,
        'breadcrumbs': build_breadcrumbs(level, lang, category_slug, country_code, city_slug, town_slug),
        'facets': facets,
        'items': business_serializer.data,
        'pagination': {
            'page': page,
            'page_size': page_size,
            'has_more': page_obj.has_next()
        }
    }
    
    return Response(response_data)


@api_view(['GET'])
def countries_list(request):
    """GET /api/countries - List all countries"""
    countries = Country.objects.filter(is_active=True).order_by('code')
    serializer = CountrySerializer(countries, many=True)
    return Response({
        'items': serializer.data,
        'count': countries.count()
    })


@api_view(['GET'])
def cities_list(request):
    """GET /api/cities - List all cities"""
    country_code = request.GET.get('country')
    cities = City.objects.filter(is_active=True)
    
    if country_code:
        cities = cities.filter(country__code=country_code)
    
    cities = cities.order_by('name')
    serializer = CitySerializer(cities, many=True)
    return Response({
        'items': serializer.data,
        'count': cities.count()
    })


@api_view(['GET'])
def towns_list(request):
    """GET /api/towns - List all towns"""
    country_code = request.GET.get('country')
    city_slug = request.GET.get('city')
    towns = Town.objects.filter(is_active=True)
    
    if country_code:
        towns = towns.filter(city__country__code=country_code)
    if city_slug:
        towns = towns.filter(city__slug=city_slug)
    
    towns = towns.order_by('name')
    serializer = TownSerializer(towns, many=True)
    return Response({
        'items': serializer.data,
        'count': towns.count()
    })


@api_view(['GET'])
def businesses_list(request):
    """GET /api/businesses - List all businesses with pagination"""
    businesses = Business.objects.filter(status='active').select_related(
        'town__city__country'
    ).prefetch_related('categories')
    
    # Filter parameters
    category_slug = request.GET.get('category')
    country_code = request.GET.get('country')
    city_slug = request.GET.get('city')
    town_slug = request.GET.get('town')
    search_query = request.GET.get('search')
    
    if category_slug:
        businesses = businesses.filter(categories__slug=category_slug)
    if country_code:
        businesses = businesses.filter(town__city__country__code=country_code)
    if city_slug:
        businesses = businesses.filter(town__city__slug=city_slug)
    if town_slug:
        businesses = businesses.filter(town__slug=town_slug)
    if search_query:
        businesses = businesses.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(categories__name_en__icontains=search_query)
        ).distinct()
    
    # Pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = min(int(request.GET.get('page_size', 20)), 100)  # Max 100 items per page
    
    total_count = businesses.count()
    businesses = businesses.order_by('name')
    
    # Apply pagination
    paginator = Paginator(businesses, page_size)
    
    try:
        businesses_page = paginator.get_page(page)
    except:
        businesses_page = paginator.get_page(1)
    
    serializer = BusinessSerializer(businesses_page, many=True)
    
    return Response({
        'items': serializer.data,
        'count': total_count,
        'pagination': {
            'page': businesses_page.number,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'has_next': businesses_page.has_next(),
            'has_previous': businesses_page.has_previous(),
            'total_count': total_count
        }
    })