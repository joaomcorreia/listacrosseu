from rest_framework import serializers
from .models import SiteSetting


class SiteSettingSerializer(serializers.ModelSerializer):
    """Serializer for site settings"""
    
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'site_tagline', 'contact_email', 'support_email', 
            'phone', 'address', 'logo', 'favicon', 'logo_url', 'favicon_url',
            'navigation_display_mode', 'enable_nav_animation', 'nav_animation_colors',
            'nav_animation_speed', 'enable_slideshow_animation', 'slideshow_animation_speed',
            'updated_at'
        ]
    
    def get_logo_url(self, obj):
        """Get full URL for logo"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def get_favicon_url(self, obj):
        """Get full URL for favicon"""
        if obj.favicon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.favicon.url)
            return obj.favicon.url
        return None


class SiteSettingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating site settings"""
    
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'site_tagline', 'contact_email', 'support_email', 
            'phone', 'address', 'logo', 'favicon', 'navigation_display_mode',
            'enable_nav_animation', 'nav_animation_colors', 'nav_animation_speed',
            'enable_slideshow_animation', 'slideshow_animation_speed'
        ]
    
    def validate_logo(self, value):
        """Validate logo file"""
        if value and value.size > 2 * 1024 * 1024:  # 2MB
            raise serializers.ValidationError("Logo file size must be under 2MB.")
        return value
    
    def validate_favicon(self, value):
        """Validate favicon file"""
        if value and value.size > 1 * 1024 * 1024:  # 1MB
            raise serializers.ValidationError("Favicon file size must be under 1MB.")
        return value