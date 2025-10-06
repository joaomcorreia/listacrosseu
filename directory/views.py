from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from businesses.models import Business, Category, Country, City


class HomeView(TemplateView):
    """Main homepage view"""
    template_name = 'directory/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_businesses'] = Business.objects.filter(
            status='active', featured=True
        )[:6]
        context['categories'] = Category.objects.filter(
            is_active=True, parent=None
        )[:8]
        context['countries'] = Country.objects.filter(is_active=True)
        return context


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'directory/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None)


class CategoryDetailView(DetailView):
    """Category detail page"""
    model = Category
    template_name = 'directory/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['businesses'] = Business.objects.filter(
            category=category, status='active'
        )[:20]
        context['subcategories'] = category.subcategories.filter(is_active=True)
        return context


class CountryView(TemplateView):
    """Country detail page"""
    template_name = 'directory/country_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_code = kwargs.get('country_code').upper()  # Convert to uppercase
        country = get_object_or_404(Country, code=country_code)
        
        businesses = Business.objects.filter(city__country=country, status='active')
        cities = City.objects.filter(country=country)
        
        context['country'] = country
        context['businesses'] = businesses[:20]
        context['cities'] = cities[:10]
        context['businesses_count'] = businesses.count()
        context['cities_count'] = cities.count()
        context['categories'] = Category.objects.filter(is_active=True, parent=None)
        return context


class CityView(TemplateView):
    """City detail page"""
    template_name = 'directory/city_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_name = kwargs.get('city_name')
        city = get_object_or_404(City, name=city_name)
        
        businesses = Business.objects.filter(city=city, status='active')
        
        context['city'] = city
        context['businesses'] = businesses
        context['businesses_count'] = businesses.count()
        context['categories'] = Category.objects.filter(is_active=True, parent=None)
        return context


class BusinessDetailView(DetailView):
    """Business detail page"""
    model = Business
    template_name = 'directory/business_detail.html'
    context_object_name = 'business'
    
    def get_queryset(self):
        return Business.objects.filter(status='active')
    
    def get_object(self):
        business = super().get_object()
        # Increment view count
        business.views_count += 1
        business.save(update_fields=['views_count'])
        return business


class SearchView(TemplateView):
    """Search results page"""
    template_name = 'directory/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            from django.db.models import Q
            context['businesses'] = Business.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query),
                status='active'
            )[:50]
        else:
            context['businesses'] = Business.objects.none()
        
        context['query'] = query
        return context


# Commented out - websites app moved to dev_archive
# class WebsiteView(TemplateView):
#     """User website view (handled by middleware)"""
#     template_name = 'websites/user_website.html'
#     
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         
#         if hasattr(self.request, 'website'):
#             website = self.request.website
#             context['website'] = website
#             context['businesses'] = Business.objects.filter(
#                 owner=website.user, status='active'
#             )
#         
#         return context


# API Views (simplified versions without DRF)
class BusinessListAPIView(TemplateView):
    """Simple API view for business listings"""
    
    def get(self, request, *args, **kwargs):
        businesses = Business.objects.filter(status='active')[:20]
        data = []
        
        for business in businesses:
            data.append({
                'id': str(business.id),
                'name': business.name,
                'description': business.short_description or business.description[:200],
                'city': business.city.name if business.city else None,
                'country': business.city.country.name if business.city else None,
                'category': business.category.name if business.category else None,
                'rating': business.average_rating,
                'website': business.website,
                'phone': business.phone,
            })
        
        return JsonResponse({'results': data})


class SearchAPIView(TemplateView):
    """Simple API view for search"""
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        data = []
        
        if query:
            from django.db.models import Q
            businesses = Business.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query),
                status='active'
            )[:10]
            
            for business in businesses:
                data.append({
                    'id': str(business.id),
                    'name': business.name,
                    'description': business.short_description or business.description[:200],
                    'city': business.city.name if business.city else None,
                    'category': business.category.name if business.category else None,
                })
        
        return JsonResponse({'results': data, 'query': query})