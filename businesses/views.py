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
    from rest_framework.decorators import api_view
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
        category = self.request.query_params.get('category', None)
        country = self.request.query_params.get('country', None)
        city = self.request.query_params.get('city', None)
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if country:
            queryset = queryset.filter(city__country__code=country)
        if city:
            queryset = queryset.filter(city__name__icontains=city)
            
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for categories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for countries"""
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CategorySerializer  # Will create CountrySerializer later


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