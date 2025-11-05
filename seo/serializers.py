from rest_framework import serializers
from .models import Country, Language, SeoPlan, SeoPage, SeoContentBlock


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'name', 'default_locale']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name']


class SeoPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoPlan
        fields = ['id', 'name', 'slug', 'features', 'order']


class SeoContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoContentBlock
        fields = ['id', 'key', 'content', 'order']


class SeoPageSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    plan = SeoPlanSerializer(read_only=True)
    content_blocks = SeoContentBlockSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    can_use_growth_features = serializers.SerializerMethodField()
    can_use_premium_features = serializers.SerializerMethodField()
    
    class Meta:
        model = SeoPage
        fields = [
            'id', 'country', 'language', 'slug', 'page_type', 'plan',
            
            # Basic SEO fields (always included)
            'meta_title', 'meta_description', 'h1', 'h2', 
            'canonical_url', 'robots', 'image_alt_fallback',
            
            # Growth fields (conditionally included)
            'keywords_hint', 'internal_links', 'sitemap_include',
            'og_title', 'og_description', 'og_image_url',
            'twitter_card', 'twitter_image_url',
            
            # Premium fields (conditionally included) 
            'json_ld', 'breadcrumbs', 'local_business_schema', 'service_schema',
            
            # Meta fields
            'is_published', 'publish_at', 'created_at', 'updated_at',
            'content_blocks', 'absolute_url', 'can_use_growth_features', 'can_use_premium_features'
        ]
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_can_use_growth_features(self, obj):
        return obj.plan.order >= 1
    
    def get_can_use_premium_features(self, obj):
        return obj.plan.order >= 2
    
    def validate(self, data):
        """Validate plan restrictions on field updates"""
        if self.instance:  # Update operation
            plan = self.instance.plan
            
            # Check Growth features
            growth_fields = [
                'keywords_hint', 'internal_links', 'sitemap_include',
                'og_title', 'og_description', 'og_image_url',
                'twitter_card', 'twitter_image_url'
            ]
            
            # Check Premium features
            premium_fields = [
                'json_ld', 'breadcrumbs', 'local_business_schema', 'service_schema'
            ]
            
            if plan.order < 1:  # Basic plan
                for field in growth_fields + premium_fields:
                    if field in data and data[field]:
                        raise serializers.ValidationError({
                            field: f"This feature requires Growth or Premium plan. Current plan: {plan.name}"
                        })
            
            elif plan.order < 2:  # Growth plan
                for field in premium_fields:
                    if field in data and data[field]:
                        raise serializers.ValidationError({
                            field: f"This feature requires Premium plan. Current plan: {plan.name}"
                        })
        
        return data
    
    def to_representation(self, instance):
        """Filter out fields based on plan restrictions"""
        data = super().to_representation(instance)
        
        # Growth features
        if instance.plan.order < 1:
            growth_fields = [
                'keywords_hint', 'internal_links', 'sitemap_include',
                'og_title', 'og_description', 'og_image_url',
                'twitter_card', 'twitter_image_url'
            ]
            for field in growth_fields:
                data.pop(field, None)
        
        # Premium features 
        if instance.plan.order < 2:
            premium_fields = [
                'json_ld', 'breadcrumbs', 'local_business_schema', 'service_schema'
            ]
            for field in premium_fields:
                data.pop(field, None)
        
        return data


class SitemapSerializer(serializers.ModelSerializer):
    """Simplified serializer for sitemap generation"""
    url = serializers.SerializerMethodField()
    country_code = serializers.CharField(source='country.code', read_only=True)
    language_code = serializers.CharField(source='language.code', read_only=True)
    
    class Meta:
        model = SeoPage
        fields = [
            'url', 'country_code', 'language_code', 'page_type',
            'updated_at', 'publish_at'
        ]
    
    def get_url(self, obj):
        return obj.get_absolute_url()