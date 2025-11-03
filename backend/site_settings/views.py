from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import SiteSetting
from .serializers import SiteSettingSerializer, SiteSettingUpdateSerializer


class SiteSettingView(APIView):
    """API view for site settings"""
    
    def get(self, request):
        """Get current site settings"""
        settings = SiteSetting.get_settings()
        serializer = SiteSettingSerializer(settings, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        """Update site settings"""
        settings = SiteSetting.get_settings()
        serializer = SiteSettingUpdateSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # Return updated settings
            response_serializer = SiteSettingSerializer(settings, context={'request': request})
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        """Partially update site settings"""
        return self.put(request)


class LogoView(APIView):
    """Dedicated view for logo operations"""
    
    def post(self, request):
        """Upload new logo"""
        settings = SiteSetting.get_settings()
        
        if 'logo' not in request.FILES:
            return Response({'error': 'No logo file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        logo_file = request.FILES['logo']
        
        # Validate file size
        if logo_file.size > 2 * 1024 * 1024:  # 2MB
            return Response({'error': 'Logo file size must be under 2MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update logo
        settings.logo = logo_file
        settings.save()
        
        serializer = SiteSettingSerializer(settings, context={'request': request})
        return Response(serializer.data)
    
    def delete(self, request):
        """Remove current logo"""
        settings = SiteSetting.get_settings()
        if settings.logo:
            settings.logo.delete(save=True)
        
        serializer = SiteSettingSerializer(settings, context={'request': request})
        return Response(serializer.data)


class FaviconView(APIView):
    """Dedicated view for favicon operations"""
    
    def post(self, request):
        """Upload new favicon"""
        settings = SiteSetting.get_settings()
        
        if 'favicon' not in request.FILES:
            return Response({'error': 'No favicon file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        favicon_file = request.FILES['favicon']
        
        # Validate file size
        if favicon_file.size > 1 * 1024 * 1024:  # 1MB
            return Response({'error': 'Favicon file size must be under 1MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update favicon
        settings.favicon = favicon_file
        settings.save()
        
        serializer = SiteSettingSerializer(settings, context={'request': request})
        return Response(serializer.data)
    
    def delete(self, request):
        """Remove current favicon"""
        settings = SiteSetting.get_settings()
        if settings.favicon:
            settings.favicon.delete(save=True)
        
        serializer = SiteSettingSerializer(settings, context={'request': request})
        return Response(serializer.data)
