from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    meta = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = ("id", "slug", "language", "is_published", "template_key", "title", "body", "meta", "updated_at")
    
    def get_meta(self, obj):
        return {
            "title": obj.seo_title(),
            "description": obj.meta_description,
            "canonical": obj.canonical_url,
            "noindex": obj.noindex,
            "nofollow": obj.nofollow,
            "og_image": obj.og_image,
            "json": obj.meta_json or {},
        }