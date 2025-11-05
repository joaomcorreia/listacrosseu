from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import activate, get_language
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from .models import Business, Category, CSVUpload
from .serializers import BusinessSerializer, BusinessListSerializer, CategorySerializer
from .services.csv_processor import process_csv_upload
from .services.large_csv_processor import process_large_csv_upload


class BusinessListView(generics.ListAPIView):
    """
    API endpoint for listing businesses with language support.
    URL: /api/v1/businesses/
    """
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'city', 'country', 'is_featured', 'is_verified']
    search_fields = ['name', 'description', 'description_en', 'description_fr', 'description_nl', 
                     'description_pt', 'description_de', 'description_es', 'description_ar', 
                     'city', 'country']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-is_featured', '-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle language parameter
        lang = self.request.query_params.get('lang')
        if lang:
            activate(lang)
        
        # Additional filtering based on query parameters
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset.select_related('category', 'owner').prefetch_related('images')


class BusinessDetailView(generics.RetrieveAPIView):
    """
    API endpoint for business detail.
    URL: /api/v1/businesses/{id}/
    """
    queryset = Business.objects.filter(is_active=True)
    serializer_class = BusinessSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        # Handle language parameter
        lang = request.query_params.get('lang')
        if lang:
            activate(lang)
        
        return super().retrieve(request, *args, **kwargs)


class CategoryListView(generics.ListAPIView):
    """
    API endpoint for listing categories.
    URL: /api/v1/categories/
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        # Handle language parameter
        lang = self.request.query_params.get('lang')
        if lang:
            activate(lang)
        
        return super().get_queryset()


@api_view(['GET'])
def business_search(request):
    """
    Advanced business search with language support
    URL: /api/v1/businesses/search/
    """
    query = request.query_params.get('q', '')
    lang = request.query_params.get('lang', 'en')
    category = request.query_params.get('category')
    city = request.query_params.get('city')
    country = request.query_params.get('country')
    
    # Activate the requested language
    activate(lang)
    
    # Build the query
    businesses = Business.objects.filter(is_active=True)
    
    if query:
        # Search in multiple language fields based on the current language
        search_fields = Q(name__icontains=query) | Q(description__icontains=query)
        
        if lang == 'en':
            search_fields |= Q(description_en__icontains=query)
        elif lang == 'fr':
            search_fields |= Q(description_fr__icontains=query)
        elif lang == 'nl':
            search_fields |= Q(description_nl__icontains=query)
        elif lang == 'pt':
            search_fields |= Q(description_pt__icontains=query)
        elif lang == 'de':
            search_fields |= Q(description_de__icontains=query)
        elif lang == 'es':
            search_fields |= Q(description_es__icontains=query)
        elif lang == 'ar':
            search_fields |= Q(description_ar__icontains=query)
            
        businesses = businesses.filter(search_fields)
    
    if category:
        businesses = businesses.filter(category__slug=category)
    
    if city:
        businesses = businesses.filter(city__icontains=city)
        
    if country:
        businesses = businesses.filter(country__icontains=country)
    
    # Order results
    businesses = businesses.select_related('category', 'owner').prefetch_related('images')
    businesses = businesses.order_by('-is_featured', '-is_verified', '-created_at')
    
    # Paginate results
    from django.core.paginator import Paginator
    paginator = Paginator(businesses, 20)
    page_number = request.query_params.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    serializer = BusinessListSerializer(page_obj, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'language': get_language(),
    })


class BusinessSearchView(APIView):
    """
    Advanced business search API for frontend search functionality
    URL: /api/v1/search/businesses/
    """
    
    def get(self, request):
        # Extract query parameters
        q = request.GET.get('q', '').strip()
        country = request.GET.get('country')
        city = request.GET.get('city')
        category = request.GET.get('category')
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        lang = request.GET.get('lang', 'en')
        
        # Activate the requested language
        activate(lang)
        
        # Start with all active businesses
        qs = Business.objects.filter(is_active=True)
        
        # Apply text search across multiple fields
        if q:
            # Search in multiple language fields based on current language
            search_fields = Q(name__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q)
            
            # Add language-specific description fields
            if lang == 'en' and hasattr(Business, 'description_en'):
                search_fields |= Q(description_en__icontains=q)
            elif lang == 'fr' and hasattr(Business, 'description_fr'):
                search_fields |= Q(description_fr__icontains=q)
            elif lang == 'nl' and hasattr(Business, 'description_nl'):
                search_fields |= Q(description_nl__icontains=q)
            elif lang == 'pt' and hasattr(Business, 'description_pt'):
                search_fields |= Q(description_pt__icontains=q)
            elif lang == 'de' and hasattr(Business, 'description_de'):
                search_fields |= Q(description_de__icontains=q)
            elif lang == 'es' and hasattr(Business, 'description_es'):
                search_fields |= Q(description_es__icontains=q)
            elif lang == 'ar' and hasattr(Business, 'description_ar'):
                search_fields |= Q(description_ar__icontains=q)
                
            qs = qs.filter(search_fields)
        
        # Apply filters
        if country:
            qs = qs.filter(country__iexact=country)
        if city:
            qs = qs.filter(city__iexact=city)
        if category:
            qs = qs.filter(category__name__iexact=category)
        
        # Get total count before pagination
        total = qs.count()
        
        # Apply ordering and pagination
        items = qs.select_related('category', 'owner').prefetch_related('images')
        items = items.order_by('-is_featured', '-is_verified', 'name')[offset:offset+limit]
        
        # Serialize results
        serializer = BusinessListSerializer(items, many=True, context={'request': request})
        
        return Response({
            'total': total,
            'results': serializer.data,
            'query': q,
            'language': get_language(),
            'limit': limit,
            'offset': offset,
            'has_more': total > (offset + limit)
        })


class FeaturedBusinesses(APIView):
    """
    API endpoint for featured businesses with country/EU scope support.
    URL: /api/v1/featured/
    Query params:
    - country: filter by specific country (e.g., 'PT', 'FR')
    - scope: 'EU' for EU-wide featured businesses
    - limit: number of results to return (default: 12)
    """
    
    def get(self, request):
        country = (request.GET.get("country") or "").strip()
        scope = (request.GET.get("scope") or "").strip().upper()
        limit = int(request.GET.get("limit", 12))
        
        # Base queryset - only active and featured businesses
        qs = Business.objects.filter(is_active=True, is_featured=True)

        if scope == "EU":
            # EU-wide = no country filter, show all featured across Europe
            pass
        elif country:
            # Country-specific featured businesses
            qs = qs.filter(country__iexact=country)
        
        # Select related for better performance and order by name
        items = qs.select_related('category', 'owner').order_by('name')[:limit]
        
        # Serialize the results
        serializer = BusinessListSerializer(items, many=True, context={'request': request})
        
        return Response({
            "results": serializer.data,
            "country": country,
            "scope": scope,
            "total": len(serializer.data)
        })


# CSV Upload Views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def csv_upload_view(request):
    """
    Django template view for CSV upload (Admin interface)
    """
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'No file was uploaded.')
            return redirect('csv_upload')
        
        csv_file = request.FILES['csv_file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('csv_upload')
        
        # Create CSV upload record
        csv_upload = CSVUpload.objects.create(
            file=csv_file,
            uploaded_by=request.user
        )
        
        # Process the CSV file (choose processor based on file size)
        try:
            file_size = csv_upload.file.size
            if file_size > 1024 * 1024:  # Use optimized processor for files > 1MB
                result = process_large_csv_upload(csv_upload.id)
                if result['success']:
                    messages.success(
                        request, 
                        f"Large CSV processing completed! {result['successful_count']} businesses imported successfully."
                        + (f" {result['failed_count']} rows failed." if result['failed_count'] > 0 else "")
                    )
                else:
                    messages.error(request, f"CSV processing failed: {result['message']}")
            else:
                result = process_csv_upload(csv_upload.id)
                if result['success']:
                    messages.success(
                        request, 
                        f"CSV processing completed! {result['successful_count']} businesses imported successfully."
                        + (f" {result['failed_count']} rows failed." if result['failed_count'] > 0 else "")
                    )
                else:
                    messages.error(request, f"CSV processing failed: {result['message']}")
        except Exception as e:
            messages.error(request, f"Error processing CSV: {str(e)}")
        
        return redirect('csv_upload')
    
    # GET request - show upload form and recent uploads
    recent_uploads = CSVUpload.objects.filter(
        uploaded_by=request.user
    ).order_by('-uploaded_at')[:10]
    
    return render(request, 'listings/csv_upload.html', {
        'recent_uploads': recent_uploads
    })


class CSVUploadAPIView(APIView):
    """
    API endpoint for CSV upload (for API clients or admin panel)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        if 'csv_file' not in request.FILES:
            return Response(
                {'error': 'No file was uploaded'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['csv_file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'Please upload a CSV file'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create CSV upload record
        csv_upload = CSVUpload.objects.create(
            file=csv_file,
            uploaded_by=request.user
        )
        
        # Process the CSV file
        try:
            result = process_csv_upload(csv_upload.id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        """Get list of CSV uploads for the current user"""
        uploads = CSVUpload.objects.filter(
            uploaded_by=request.user
        ).order_by('-uploaded_at')[:20]
        
        data = []
        for upload in uploads:
            data.append({
                'id': upload.id,
                'filename': upload.file.name.split('/')[-1],
                'uploaded_at': upload.uploaded_at,
                'status': upload.status,
                'total_rows': upload.total_rows,
                'successful_rows': upload.successful_rows,
                'failed_rows': upload.failed_rows,
                'processed_at': upload.processed_at,
            })
        
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def csv_upload_status(request, upload_id):
    """
    API endpoint to check the status of a specific CSV upload
    """
    try:
        upload = CSVUpload.objects.get(id=upload_id, uploaded_by=request.user)
        
        return Response({
            'id': upload.id,
            'filename': upload.file.name.split('/')[-1],
            'status': upload.status,
            'uploaded_at': upload.uploaded_at,
            'processed_at': upload.processed_at,
            'total_rows': upload.total_rows,
            'successful_rows': upload.successful_rows,
            'failed_rows': upload.failed_rows,
            'error_log': upload.error_log,
            'processing_notes': upload.processing_notes,
        }, status=status.HTTP_200_OK)
        
    except CSVUpload.DoesNotExist:
        return Response(
            {'error': 'CSV upload not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def csv_upload_progress(request, upload_id):
    """
    API endpoint to get real-time progress of CSV processing
    """
    try:
        upload = CSVUpload.objects.get(id=upload_id, uploaded_by=request.user)
        
        # Get progress from cache
        from listings.services.large_csv_processor import LargeCSVProcessor
        processor = LargeCSVProcessor(upload)
        progress_data = processor.get_progress()
        
        # Add upload status info
        progress_data.update({
            'upload_id': upload.id,
            'filename': upload.file.name.split('/')[-1],
            'status': upload.status,
            'total_rows': upload.total_rows,
        })
        
        return Response(progress_data, status=status.HTTP_200_OK)
        
    except CSVUpload.DoesNotExist:
        return Response(
            {'error': 'CSV upload not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def countries_list(request):
    """
    API endpoint for countries with business counts
    URL: /api/v1/countries/
    """
    lang = request.query_params.get('lang', 'en')
    activate(lang)
    
    countries = Business.objects.filter(is_active=True)\
        .values('country')\
        .annotate(business_count=Count('id'))\
        .order_by('country')
    
    return Response({
        'countries': list(countries),
        'total_countries': countries.count()
    })


@api_view(['GET'])
def cities_list(request):
    """
    API endpoint for cities with business counts
    URL: /api/v1/cities/
    """
    lang = request.query_params.get('lang', 'en')
    activate(lang)
    
    country = request.query_params.get('country')
    
    cities_query = Business.objects.filter(is_active=True)
    if country:
        cities_query = cities_query.filter(country__iexact=country)
    
    cities = cities_query.values('city', 'country')\
        .annotate(business_count=Count('id'))\
        .order_by('country', 'city')
    
    return Response({
        'cities': list(cities),
        'total_cities': cities.count(),
        'filtered_by_country': country
    })


@api_view(['GET'])
def categories_with_counts(request):
    """
    API endpoint for categories with business counts
    URL: /api/v1/categories/counts/
    """
    lang = request.query_params.get('lang', 'en')
    activate(lang)
    
    categories = Category.objects.filter(is_active=True)\
        .annotate(business_count=Count('business', filter=Q(business__is_active=True)))\
        .order_by('name')
    
    category_data = []
    for category in categories:
        category_data.append({
            'id': category.id,
            'name': category.name,
            'name_localized': category.get_name_for_language(lang),
            'slug': category.slug,
            'description': category.description,
            'business_count': category.business_count
        })
    
    return Response({
        'categories': category_data,
        'total_categories': len(category_data),
        'language': lang
    })


@api_view(['GET'])
def businesses_by_country(request, country):
    """
    API endpoint for businesses filtered by country
    URL: /api/v1/countries/{country}/businesses/
    """
    lang = request.query_params.get('lang', 'en')
    activate(lang)
    
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    category = request.query_params.get('category')
    city = request.query_params.get('city')
    
    businesses_query = Business.objects.filter(
        is_active=True,
        country__iexact=country
    ).select_related('category')
    
    if category:
        businesses_query = businesses_query.filter(category__slug=category)
    if city:
        businesses_query = businesses_query.filter(city__iexact=city)
    
    total_count = businesses_query.count()
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    businesses = businesses_query[start:end]
    
    # Serialize the businesses
    serializer = BusinessListSerializer(businesses, many=True, context={'request': request})
    
    return Response({
        'businesses': serializer.data,
        'country': country,
        'total_count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size,
        'filters': {
            'category': category,
            'city': city,
            'language': lang
        }
    })