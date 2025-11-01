from rest_framework import serializers
from catalog.models import Category, Business
from geo.models import Country, City, Town


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['slug', 'name', 'count']
    
    def get_name(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_name(lang)


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Country
        fields = ['code', 'name', 'count']
    
    def get_name(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_name(lang)


class CitySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = City
        fields = ['slug', 'name', 'count']


class TownSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Town
        fields = ['slug', 'name', 'count']


class BusinessSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    town_name = serializers.CharField(source='town.name', read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'slug', 'name', 'city_name', 'town_name', 'country_id',
            'street', 'postcode', 'phone', 'email', 'website'
        ]


class BreadcrumbSerializer(serializers.Serializer):
    label = serializers.CharField()
    href = serializers.CharField()


class FacetSerializer(serializers.Serializer):
    countries = CountrySerializer(many=True, required=False)
    cities = CitySerializer(many=True, required=False)
    towns = TownSerializer(many=True, required=False)


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_more = serializers.BooleanField()


class UniformResponseSerializer(serializers.Serializer):
    level = serializers.CharField()
    breadcrumbs = BreadcrumbSerializer(many=True)
    facets = FacetSerializer()
    items = serializers.ListField(child=serializers.DictField())
    pagination = PaginationSerializer()