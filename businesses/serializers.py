from rest_framework import serializers
from .models import Business, Category, Country, City, Review


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active']


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for countries"""
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'is_eu_member', 'is_active']


class CitySerializer(serializers.ModelSerializer):
    """Serializer for cities"""
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'latitude', 'longitude', 'population']


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for businesses"""
    category = CategorySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'email', 'phone', 'website', 'address', 'city', 'category',
            'logo', 'cover_image', 'plan', 'status', 'featured', 'verified',
            'average_rating', 'review_count', 'views_count', 'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'title', 'content', 'reviewer_name',
            'owner_response', 'response_date', 'created_at'
        ]