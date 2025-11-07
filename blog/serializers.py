from rest_framework import serializers
from .models import BlogPost, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description']
    
    def get_name(self, obj):
        """Get category name in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_name(lang)
    
    def get_description(self, obj):
        """Get category description in requested language"""  
        lang = self.context.get('lang', 'en')
        return obj.get_description(lang)


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image', 
            'published_at', 'category', 'author_name', 'is_featured', 'status'
        ]
    
    def get_title(self, obj):
        """Get title in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_title(lang)
    
    def get_excerpt(self, obj):
        """Get excerpt in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_excerpt(lang)
    
    def get_author_name(self, obj):
        """Get author name with fallback"""
        if obj.author:
            full_name = obj.author.get_full_name().strip()
            if full_name:
                return full_name
            return obj.author.username or 'Anonymous'
        return 'Anonymous'


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'cover_image',
            'published_at', 'category', 'author_name', 'is_featured',
            # SEO fields
            'meta_title', 'meta_description', 'canonical_url', 'robots',
            'og_title', 'og_description', 'og_image'
        ]
    
    def get_title(self, obj):
        """Get title in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_title(lang)
    
    def get_excerpt(self, obj):
        """Get excerpt in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_excerpt(lang)
        
    def get_content(self, obj):
        """Get content in requested language"""
        lang = self.context.get('lang', 'en')
        return obj.get_content(lang)


class BlogPostAdminSerializer(serializers.ModelSerializer):
    """Admin serializer for creating and editing blog posts"""
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title_en', 'slug', 'excerpt_en', 'content_en', 'cover_image',
            'published_at', 'category', 'category_id', 'author_name', 'is_featured', 'status',
            # SEO fields
            'meta_title', 'meta_description', 'canonical_url', 'robots',
            'og_title', 'og_description', 'og_image'
        ]
        extra_kwargs = {
            'slug': {'required': False},
            'published_at': {'required': False},
        }
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        if category_id:
            try:
                validated_data['category'] = BlogCategory.objects.get(id=category_id)
            except BlogCategory.DoesNotExist:
                pass
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        if category_id:
            try:
                validated_data['category'] = BlogCategory.objects.get(id=category_id)
            except BlogCategory.DoesNotExist:
                pass
        return super().update(instance, validated_data)