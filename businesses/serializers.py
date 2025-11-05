from rest_framework import serializers
from .models import Business, Category, Country, City, Review


class CountrySerializer(serializers.ModelSerializer):
    """Enhanced serializer for Country model with API support"""
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'slug', 'flag_image', 'is_eu_member', 'is_active']


class CitySerializer(serializers.ModelSerializer):
    """Enhanced serializer for City model with country details"""
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = City
        fields = [
            'id', 'name', 'slug', 'country', 'country_id',
            'latitude', 'longitude', 'population', 'is_capital'
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Enhanced serializer for Category model with hierarchy support"""
    parent = serializers.StringRelatedField(read_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subcategories = serializers.StringRelatedField(many=True, read_only=True)
    full_path = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'parent', 'parent_id', 'subcategories', 'full_path',
            'is_active', 'sort_order', 'created_at', 'updated_at'
        ]


class BusinessListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for business listings"""
    city = serializers.StringRelatedField(read_only=True)
    country = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'short_description', 'email', 'phone',
            'website', 'address', 'city', 'country', 'category',
            'latitude', 'longitude', 'plan', 'status', 'featured',
            'verified', 'views_count', 'clicks_count'
        ]
    
    def get_country(self, obj):
        return obj.city.country.name if obj.city else None


class BusinessSerializer(serializers.ModelSerializer):
    """Complete serializer for business details with multilingual support"""
    city = CitySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    
    # Translations field for 27 EU languages
    translations = serializers.JSONField(required=False, default=dict)
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'email', 'phone', 'website', 'address', 'postal_code',
            'city', 'city_id', 'category', 'category_id',
            'latitude', 'longitude', 'plan', 'status', 'featured',
            'verified', 'views_count', 'clicks_count',
            'meta_title', 'meta_description', 'keywords',
            'monday_hours', 'tuesday_hours', 'wednesday_hours',
            'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours',
            'translations', 'average_rating', 'review_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'views_count', 'clicks_count']

    def validate_translations(self, value):
        """Validate translations field structure for 27 EU languages"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Translations must be a dictionary")
        
        # EU language codes
        valid_languages = [
            'bg', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'el', 'hu',
            'ga', 'it', 'lv', 'lt', 'mt', 'pl', 'pt', 'ro', 'sk', 'sl', 'es', 'sv',
            'no', 'is', 'ch'
        ]
        
        for lang_code, translation_data in value.items():
            if lang_code not in valid_languages:
                raise serializers.ValidationError(f"Invalid language code: {lang_code}")
            
            if not isinstance(translation_data, dict):
                raise serializers.ValidationError(f"Translation for {lang_code} must be a dictionary")
        
        return value


class BusinessCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new businesses"""
    
    class Meta:
        model = Business
        fields = [
            'name', 'description', 'short_description', 'email', 'phone',
            'website', 'address', 'postal_code', 'city_id', 'category_id',
            'latitude', 'longitude', 'monday_hours', 'tuesday_hours',
            'wednesday_hours', 'thursday_hours', 'friday_hours',
            'saturday_hours', 'sunday_hours', 'translations'
        ]

    def validate_email(self, value):
        """Ensure unique email per city (preserving your duplicate prevention logic)"""
        city_id = self.initial_data.get('city_id')
        if city_id and Business.objects.filter(email=value, city_id=city_id).exists():
            raise serializers.ValidationError("A business with this email already exists in this city.")
        return value

    def validate_phone(self, value):
        """Ensure unique phone per city (preserving your duplicate prevention logic)"""
        city_id = self.initial_data.get('city_id')
        if city_id and Business.objects.filter(phone=value, city_id=city_id).exists():
            raise serializers.ValidationError("A business with this phone number already exists in this city.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'title', 'content', 'reviewer_name',
            'owner_response', 'response_date', 'created_at'
        ]