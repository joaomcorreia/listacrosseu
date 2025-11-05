from rest_framework import serializers
from django.utils.translation import get_language
from .models import Business, Category, BusinessImage


class CategorySerializer(serializers.ModelSerializer):
    localized_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'localized_name', 'slug', 'description', 'is_active']
    
    def get_localized_name(self, obj):
        """Get category name in current language"""
        current_language = get_language()
        return obj.get_name_for_language(current_language)


class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ['id', 'image', 'caption', 'is_primary', 'order']


class BusinessSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = BusinessImageSerializer(many=True, read_only=True)
    localized_description = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'description', 'localized_description', 'category', 'owner_name',
            'email', 'phone', 'website', 'address', 'city', 'country', 'postal_code',
            'latitude', 'longitude', 'is_active', 'is_featured', 'is_verified',
            'slug', 'meta_title', 'meta_description', 'images', 'created_at', 'updated_at'
        ]
    
    def get_localized_description(self, obj):
        """Get business description in current language"""
        current_language = get_language()
        return obj.get_description_for_language(current_language)


class BusinessListSerializer(serializers.ModelSerializer):
    """Serializer for business list view (lighter data)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    localized_description = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'localized_description', 'category_name', 'city', 'country',
            'is_active', 'is_public', 'is_featured', 'is_verified', 'slug', 'primary_image', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        """Get primary business image"""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None
    
    def get_localized_description(self, obj):
        """Get business description in current language (truncated)"""
        current_language = get_language()
        description = obj.get_description_for_language(current_language)
        return description[:200] + '...' if len(description) > 200 else description