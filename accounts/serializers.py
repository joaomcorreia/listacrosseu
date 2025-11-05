from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['arabic_on_dashboard', 'arabic_on_website', 'preferred_language']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        
        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['arabic_on_dashboard', 'arabic_on_website', 'preferred_language']
        
    def update(self, instance, validated_data):
        """Update user profile with language preferences"""
        instance.arabic_on_dashboard = validated_data.get('arabic_on_dashboard', instance.arabic_on_dashboard)
        instance.arabic_on_website = validated_data.get('arabic_on_website', instance.arabic_on_website)
        instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
        instance.save()
        return instance