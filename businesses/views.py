from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db import models
from .models import Business, Category, Country, City, Review

# DRF imports with try/except for graceful handling
try:
    from rest_framework import generics, viewsets, status
    from rest_framework.decorators import api_view, action
    from rest_framework.response import Response
    from .serializers import BusinessSerializer, CategorySerializer
    DRF_AVAILABLE = True
except ImportError:
    DRF_AVAILABLE = False


class BusinessViewSet(viewsets.ModelViewSet):
    """API viewset for businesses"""
    queryset = Business.objects.filter(status='active')
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        queryset = Business.objects.filter(status='active')
        
        # Filter parameters
        category = self.request.query_params.get('category', None)
        country = self.request.query_params.get('country', None)
        city = self.request.query_params.get('city', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category__icontains=category)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(description__icontains=search) |
                models.Q(city__icontains=search) |
                models.Q(country__icontains=search)
            )
            
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get business statistics"""
        try:
            total_businesses = Business.objects.filter(status='active').count()
            
            # Count countries that have businesses
            countries_with_businesses = Business.objects.filter(status='active')\
                .values('city__country__name')\
                .distinct()\
                .count()
            
            # Count cities that have businesses  
            cities_with_businesses = Business.objects.filter(status='active')\
                .values('city__name')\
                .distinct()\
                .count()
                
            # Count categories that have businesses
            categories_with_businesses = Business.objects.filter(status='active')\
                .values('category__name')\
                .distinct()\
                .count()
            
            return Response({
                'total_businesses': total_businesses,
                'countries': countries_with_businesses,
                'cities': cities_with_businesses,
                'categories': categories_with_businesses
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def countries(self, request):
        """Get list of countries with businesses"""
        try:
            countries = Business.objects.filter(status='active')\
                .select_related('city__country')\
                .values_list('city__country__name', flat=True)\
                .distinct()\
                .order_by('city__country__name')
            return Response(list(countries))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Get list of cities, optionally filtered by country"""
        try:
            queryset = Business.objects.filter(status='active').select_related('city__country')
            country = request.query_params.get('country', None)
            
            if country:
                queryset = queryset.filter(city__country__name__icontains=country)
            
            cities = queryset.values_list('city__name', flat=True)\
                .distinct()\
                .order_by('city__name')
            return Response(list(cities))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of business categories"""
        try:
            categories = Business.objects.filter(status='active')\
                .select_related('category')\
                .values_list('category__name', flat=True)\
                .distinct()\
                .order_by('category__name')
            return Response(list(categories))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for categories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for countries"""
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CategorySerializer


@api_view(['GET'])
def business_stats(request):
    """Get business statistics"""
    try:
        total_businesses = Business.objects.filter(status='active').count()
        
        # Count countries that have businesses
        countries_with_businesses = Business.objects.filter(status='active')\
            .values('city__country__name')\
            .distinct()\
            .count()
        
        # Count cities that have businesses  
        cities_with_businesses = Business.objects.filter(status='active')\
            .values('city__name')\
            .distinct()\
            .count()
            
        # Count categories that have businesses
        categories_with_businesses = Business.objects.filter(status='active')\
            .values('category__name')\
            .distinct()\
            .count()
        
        return Response({
            'total_businesses': total_businesses,
            'countries': countries_with_businesses,
            'cities': cities_with_businesses,
            'categories': categories_with_businesses
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def business_countries(request):
    """Get list of countries with businesses"""
    try:
        countries = Business.objects.filter(status='active')\
            .select_related('city__country')\
            .values_list('city__country__name', flat=True)\
            .distinct()\
            .order_by('city__country__name')
        return Response(list(countries))
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def business_cities(request):
    """Get list of cities, optionally filtered by country"""
    try:
        queryset = Business.objects.filter(status='active').select_related('city__country')
        country = request.query_params.get('country', None)
        
        if country:
            queryset = queryset.filter(city__country__name__icontains=country)
        
        cities = queryset.values_list('city__name', flat=True)\
            .distinct()\
            .order_by('city__name')
        return Response(list(cities))
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def business_categories(request):
    """Get list of business categories"""
    try:
        categories = Business.objects.filter(status='active')\
            .select_related('category')\
            .values_list('category__name', flat=True)\
            .distinct()\
            .order_by('category__name')
        return Response(list(categories))
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Will create CountrySerializer later


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for cities"""
    queryset = City.objects.all()
    serializer_class = CategorySerializer  # Will create CitySerializer later


class ReviewViewSet(viewsets.ModelViewSet):
    """API viewset for reviews"""
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = CategorySerializer  # Will create ReviewSerializer later


class BusinessSearchView(generics.ListAPIView):
    """Search businesses by name, description, etc."""
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Business.objects.filter(
                status='active'
            ).filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(category__name__icontains=query)
            )
        return Business.objects.none()


class FeaturedBusinessesView(generics.ListAPIView):
    """Get featured businesses"""
    serializer_class = BusinessSerializer
    queryset = Business.objects.filter(status='active', featured=True)[:10]