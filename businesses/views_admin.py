from django.shortcuts import render
from django.db.models import Count, Q
from businesses.models import Country, City, Category, Business

def data_overview(request):
    """
    Comprehensive overview of all data in the system
    Shows countries, cities, categories, and business counts
    """
    
    # Get countries with business counts
    countries_data = []
    countries = Country.objects.annotate(
        total_cities=Count('cities', distinct=True),
        total_businesses=Count('cities__businesses', distinct=True)
    ).order_by('name')
    
    for country in countries:
        # Get cities for this country with business counts
        cities = City.objects.filter(country=country).annotate(
            business_count=Count('businesses')
        ).order_by('-business_count', 'name')
        
        # Get categories that have businesses in this country
        categories_with_businesses = Category.objects.filter(
            businesses__city__country=country
        ).annotate(
            business_count=Count('businesses', filter=Q(businesses__city__country=country))
        ).order_by('-business_count', 'name')
        
        countries_data.append({
            'country': country,
            'cities': cities,
            'categories_with_businesses': categories_with_businesses,
        })
    
    # Get global category statistics
    all_categories = Category.objects.annotate(
        business_count=Count('businesses')
    ).order_by('-business_count', 'name')
    
    # Categories with no businesses
    empty_categories = all_categories.filter(business_count=0)
    
    # Categories with businesses
    populated_categories = all_categories.filter(business_count__gt=0)
    
    # Top cities by business count
    top_cities = City.objects.annotate(
        business_count=Count('businesses')
    ).filter(business_count__gt=0).order_by('-business_count')[:20]
    
    context = {
        'countries_data': countries_data,
        'all_categories': all_categories,
        'empty_categories': empty_categories,
        'populated_categories': populated_categories,
        'top_cities': top_cities,
        'total_countries': countries.count(),
        'total_cities': City.objects.count(),
        'total_categories': Category.objects.count(),
        'total_businesses': Business.objects.count(),
        'countries_with_businesses': countries.filter(total_businesses__gt=0).count(),
        'cities_with_businesses': City.objects.annotate(bc=Count('businesses')).filter(bc__gt=0).count(),
        'populated_categories_count': populated_categories.count(),
        'empty_categories_count': empty_categories.count(),
    }
    
    return render(request, 'businesses/data_overview.html', context)