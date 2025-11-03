from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, BlogCategory, PricingPlan, BusinessSubscription


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'color']


class BlogPostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    reading_time = serializers.CharField(source='read_time', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'language', 'excerpt',
            'content', 'image', 'image_alt', 'category', 'tags',
            'tags_list', 'status', 'featured', 'meta_title',
            'meta_description', 'view_count', 'reading_time',
            'created_at', 'updated_at', 'published_at'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()


class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for blog post lists"""
    author = AuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'language', 'excerpt',
            'image', 'image_alt', 'category', 'featured',
            'view_count', 'read_time', 'published_at'
        ]


class PricingPlanSerializer(serializers.ModelSerializer):
    display_price = serializers.CharField(source='get_display_price', read_only=True)
    billing_display = serializers.CharField(source='get_billing_display', read_only=True)
    
    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'billing_cycle', 'features', 'max_listings', 'max_images',
            'priority_support', 'is_active', 'is_featured',
            'color_scheme', 'order', 'trial_days',
            'display_price', 'billing_display'
        ]


class BusinessSubscriptionSerializer(serializers.ModelSerializer):
    pricing_plan = PricingPlanSerializer(read_only=True)
    is_active_subscription = serializers.BooleanField(source='is_active', read_only=True)
    
    class Meta:
        model = BusinessSubscription
        fields = [
            'id', 'pricing_plan', 'status', 'start_date', 'end_date',
            'is_active_subscription', 'created_at'
        ]