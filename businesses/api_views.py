from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Business, Category, City, Country, Review
from .serializers import (
    BusinessSerializer, BusinessListSerializer, BusinessCreateSerializer,
    CategorySerializer, CitySerializer, CountrySerializer, ReviewSerializer
)


class CountryListAPIView(generics.ListAPIView):
    """API endpoint for listing all EU countries"""
    queryset = Country.objects.filter(is_active=True).order_by('name')
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']


class CityListAPIView(generics.ListAPIView):
    """API endpoint for listing cities with country filtering"""
    queryset = City.objects.select_related('country').all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'is_capital']
    search_fields = ['name', 'country__name']
    ordering_fields = ['name', 'population']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        country_code = self.request.query_params.get('country_code', None)
        if country_code:
            queryset = queryset.filter(country__code=country_code)
        return queryset


class CategoryListAPIView(generics.ListAPIView):
    """API endpoint for listing business categories"""
    queryset = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'description']


class BusinessListAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating businesses"""
    queryset = Business.objects.select_related('city__country', 'category').filter(status='active')
    serializer_class = BusinessListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'category', 'plan', 'featured', 'verified']
    search_fields = ['name', 'description', 'short_description', 'address']
    ordering_fields = ['name', 'created_at', 'views_count', 'clicks_count']
    ordering = ['-featured', '-verified', '-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BusinessCreateSerializer
        return BusinessListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by country
        country_code = self.request.query_params.get('country', None)
        if country_code:
            queryset = queryset.filter(city__country__code=country_code)
        
        # Filter by location (latitude/longitude radius)
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)
        radius = self.request.query_params.get('radius', None)
        
        if lat and lng and radius:
            # Simple radius filtering (for production, consider using PostGIS)
            try:
                lat, lng, radius = float(lat), float(lng), float(radius)
                # Basic bounding box filtering
                lat_range = radius / 111.0  # Approximate km to degrees
                lng_range = radius / (111.0 * abs(lat))
                
                queryset = queryset.filter(
                    latitude__range=[lat - lat_range, lat + lat_range],
                    longitude__range=[lng - lng_range, lng + lng_range]
                )
            except (ValueError, TypeError):
                pass
        
        return queryset


class BusinessDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for business details"""
    queryset = Business.objects.select_related('city__country', 'category')
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when business is retrieved"""
        instance = self.get_object()
        instance.views_count = (instance.views_count or 0) + 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)


class BusinessSearchAPIView(APIView):
    """Advanced search API for businesses with multilingual support"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        country_code = request.query_params.get('country', '')
        category_id = request.query_params.get('category', '')
        language = request.query_params.get('lang', 'en')
        
        if not query:
            return Response({'results': [], 'count': 0})
        
        # Base queryset
        businesses = Business.objects.select_related('city__country', 'category').filter(
            status='published'
        )
        
        # Search in multiple fields including translations
        search_filter = Q(name__icontains=query) | Q(description__icontains=query) | Q(short_description__icontains=query)
        
        # Search in translations if language is specified
        if language != 'en':
            search_filter |= Q(translations__has_key=language)
        
        businesses = businesses.filter(search_filter)
        
        # Apply filters
        if country_code:
            businesses = businesses.filter(city__country__code=country_code)
        
        if category_id:
            try:
                businesses = businesses.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass
        
        # Serialize results
        serializer = BusinessListSerializer(businesses[:50], many=True)  # Limit to 50 results
        
        return Response({
            'results': serializer.data,
            'count': len(serializer.data),
            'query': query
        })


class BusinessStatsAPIView(APIView):
    """API endpoint for business statistics"""
    
    def get(self, request):
        stats = {
            'total_businesses': Business.objects.filter(status='published').count(),
            'total_cities': City.objects.count(),
            'total_countries': Country.objects.filter(is_active=True).count(),
            'total_categories': Category.objects.filter(is_active=True).count(),
            'featured_businesses': Business.objects.filter(status='published', featured=True).count(),
            'verified_businesses': Business.objects.filter(status='published', verified=True).count(),
        }
        
        # Top countries by business count
        from django.db.models import Count
        top_countries = Country.objects.annotate(
            business_count=Count('cities__businesses', filter=Q(cities__businesses__status='published'))
        ).order_by('-business_count')[:10]
        
        stats['top_countries'] = [
            {'name': country.name, 'code': country.code, 'count': country.business_count}
            for country in top_countries
        ]
        
        return Response(stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_business_clicks(request, business_id):
    """API endpoint to increment business click count"""
    try:
        business = Business.objects.get(id=business_id, status='published')
        business.clicks_count = (business.clicks_count or 0) + 1
        business.save(update_fields=['clicks_count'])
        return Response({'success': True, 'clicks': business.clicks_count})
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for business reviews"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        return Review.objects.filter(business_id=business_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        business_id = self.kwargs.get('business_id')
        business = get_object_or_404(Business, id=business_id)
        serializer.save(business=business, reviewer=self.request.user)


# Language-specific API views for multilingual support
class BusinessTranslationAPIView(APIView):
    """API endpoint for managing business translations"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, business_id, language_code):
        """Get translation for specific language"""
        try:
            business = Business.objects.get(id=business_id)
            translations = business.translations or {}
            translation = translations.get(language_code, {})
            return Response(translation)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, business_id, language_code):
        """Update translation for specific language"""
        try:
            business = Business.objects.get(id=business_id)
            
            # Validate language code
            valid_languages = [
                'bg', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'el', 'hu',
                'ga', 'it', 'lv', 'lt', 'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv',
                'no', 'is', 'ch'
            ]
            
            if language_code not in valid_languages:
                return Response({'error': 'Invalid language code'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update translation
            translations = business.translations or {}
            translations[language_code] = request.data
            business.translations = translations
            business.save(update_fields=['translations'])
            
            return Response({'success': True, 'translation': request.data})
            
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)