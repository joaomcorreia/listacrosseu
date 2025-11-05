from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils.translation import activate
from .models import UserProfile
from .serializers import UserSerializer, UserProfileUpdateSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def update(self, request, *args, **kwargs):
        """Update user language preferences"""
        response = super().update(request, *args, **kwargs)
        
        # Activate the user's preferred language
        profile = self.get_object()
        effective_language = profile.get_effective_language()
        activate(effective_language)
        
        return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request):
    """Get current user details with profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_language_preference(request):
    """Set user language preference"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    arabic_on_dashboard = request.data.get('arabic_on_dashboard', False)
    arabic_on_website = request.data.get('arabic_on_website', False)
    preferred_language = request.data.get('preferred_language', 'en')
    
    profile.arabic_on_dashboard = arabic_on_dashboard
    profile.arabic_on_website = arabic_on_website
    profile.preferred_language = preferred_language
    profile.save()
    
    # Activate the language
    effective_language = profile.get_effective_language()
    activate(effective_language)
    
    return Response({
        'message': 'Language preference updated successfully',
        'effective_language': effective_language,
        'arabic_on_dashboard': arabic_on_dashboard,
        'arabic_on_website': arabic_on_website,
        'preferred_language': preferred_language,
    }, status=status.HTTP_200_OK)