from rest_framework import serializers
from .models import Plan, VisibilityProfile


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "key", "name", "description", "highlights", "entitlements", "priority_weight", "is_active")


class VisibilityProfileSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    
    class Meta:
        model = VisibilityProfile
        fields = ("id", "plan", "featured", "featured_weight", "include_in_sitemap", "force_noindex", "badges")