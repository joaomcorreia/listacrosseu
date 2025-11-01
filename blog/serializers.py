from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "color"]


class PostCardSerializer(serializers.ModelSerializer):
    """Lightweight serializer for post cards and lists"""
    category = CategorySerializer(read_only=True)
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    featured_image_url = serializers.CharField(source="get_featured_image_url", read_only=True)
    
    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "language", "excerpt", "category", 
            "author_name", "featured_image_url", "is_featured", 
            "published_at", "created_at"
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Full post serializer with content and SEO data"""
    category = CategorySerializer(read_only=True)
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    featured_image_url = serializers.CharField(source="get_featured_image_url", read_only=True)
    related_posts = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "language", "excerpt", "content",
            "category", "author_name", "featured_image_url", "is_featured",
            "published_at", "created_at", "updated_at", "related_posts", "meta"
        ]
    
    def get_related_posts(self, obj):
        related = obj.get_related_posts()
        return PostCardSerializer(related, many=True).data
    
    def get_meta(self, obj):
        return {
            "title": obj.seo_title(),
            "description": obj.meta_description,
            "canonical_url": obj.canonical_url,
            "noindex": obj.noindex,
            "nofollow": obj.nofollow,
            "og_image": obj.og_image.url if obj.og_image else obj.get_featured_image_url(),
            "json_ld": obj.meta_json,
        }