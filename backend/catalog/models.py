from django.db import models
from django.utils import timezone
from geo.models import Country, City, Town


class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True, help_text="Lowercase, ASCII, hyphenated")
    names_json = models.JSONField(default=dict, help_text="Translations: {'en': 'Restaurants', 'nl': 'Restaurants', 'pt': 'Restaurantes'}")
    synonyms_json = models.JSONField(default=dict, help_text="Synonyms by language: {'en': ['food', 'dining'], 'nl': ['eten']}")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['slug']
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.names_json.get('en', self.slug)
    
    def get_name(self, lang='en'):
        """Get category name in specified language, fallback to English"""
        return self.names_json.get(lang, self.names_json.get('en', self.slug))


class Business(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="Generated from name + hash for uniqueness")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='businesses')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='businesses')
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, null=True, blank=True, related_name='businesses')
    street = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    categories = models.ManyToManyField(Category, through='BusinessCategory', related_name='businesses')
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Businesses"
    
    def __str__(self):
        return f"{self.name} ({self.city.name}, {self.country.code})"


class BusinessCategory(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['business', 'category']]
        verbose_name = "Business Category"
        verbose_name_plural = "Business Categories"
    
    def __str__(self):
        return f"{self.business.name} - {self.category.slug}"