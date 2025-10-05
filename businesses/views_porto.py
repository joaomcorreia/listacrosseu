from django.shortcuts import render, get_object_or_404
from businesses.models import Business, City


def porto_businesses(request):
    """Simple page showing all Porto businesses"""
    porto = get_object_or_404(City, name='Porto', country__code='PT')
    businesses = Business.objects.filter(city=porto).select_related('category').order_by('name')
    
    context = {
        'city': porto,
        'businesses': businesses,
        'total_count': businesses.count()
    }
    
    return render(request, 'businesses/porto_businesses.html', context)