from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Q, Count
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Country, Language, SeoPlan, SeoPage, SeoContentBlock
from .serializers import (
    CountrySerializer, LanguageSerializer, SeoPlanSerializer, 
    SeoPageSerializer, SeoContentBlockSerializer, SitemapSerializer
)


@method_decorator(staff_member_required, name='dispatch')
class SeoCustomDashboardView(TemplateView):
    template_name = 'seo/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get summary statistics
        context['total_pages'] = SeoPage.objects.count()
        context['published_pages'] = SeoPage.objects.filter(is_published=True).count()
        context['draft_pages'] = SeoPage.objects.filter(is_published=False).count()
        
        # Plan distribution
        context['plan_stats'] = SeoPage.objects.values('plan__name').annotate(
            count=Count('id')
        ).order_by('plan__order')
        
        # Recent pages
        context['recent_pages'] = SeoPage.objects.select_related(
            'country', 'language', 'plan'
        ).order_by('-updated_at')[:10]
        
        # Countries and languages
        context['countries'] = Country.objects.filter(is_active=True).order_by('name')
        context['languages'] = Language.objects.filter(is_active=True).order_by('name')
        context['plans'] = SeoPlan.objects.filter(is_active=True).order_by('order')
        
        return context


# API ViewSets for the frontend
class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']


class SeoPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeoPlan.objects.filter(is_active=True)
    serializer_class = SeoPlanSerializer
    ordering = ['order']


class SeoPageViewSet(viewsets.ModelViewSet):
    queryset = SeoPage.objects.select_related('country', 'language', 'plan')
    serializer_class = SeoPageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'country__code': ['exact'],
        'language__code': ['exact'],
        'page_type': ['exact'],
        'slug': ['exact'],
        'is_published': ['exact'],
        'plan__name': ['exact'],
    }
    
    search_fields = ['meta_title', 'meta_description', 'h1', 'slug']
    ordering_fields = ['updated_at', 'created_at', 'meta_title']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by published status for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def sitemap(self, request):
        """Generate sitemap data for published pages"""
        pages = SeoPage.objects.filter(
            is_published=True,
            sitemap_include=True
        ).select_related('country', 'language')
        
        serializer = SitemapSerializer(pages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish/unpublish a page"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        page = self.get_object()
        page.is_published = not page.is_published
        page.updated_by = request.user
        page.save()
        
        return Response({
            'status': 'published' if page.is_published else 'unpublished',
            'is_published': page.is_published
        })


class SeoContentBlockViewSet(viewsets.ModelViewSet):
    serializer_class = SeoContentBlockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['seo_page', 'key', 'is_active']
    
    def get_queryset(self):
        return SeoContentBlock.objects.filter(
            is_active=True,
            seo_page__is_published=True
        ).select_related('seo_page')
