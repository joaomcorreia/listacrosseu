from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True, help_text="ISO-2 country code")
    names_json = models.JSONField(default=dict, help_text="Translations: {'en': 'Portugal', 'nl': 'Portugal', 'pt': 'Portugal'}")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['code']
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.names_json.get('en', self.code)
    
    def get_name(self, lang='en'):
        """Get country name in specified language, fallback to English"""
        return self.names_json.get(lang, self.names_json.get('en', self.code))


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    slug = models.SlugField(max_length=100, help_text="Lowercase, ASCII, hyphenated")
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['country', 'name']
        unique_together = [['country', 'slug']]
        verbose_name_plural = "Cities"
    
    def __str__(self):
        return f"{self.name}, {self.country.code}"


class Town(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='towns')
    slug = models.SlugField(max_length=100, help_text="Lowercase, ASCII, hyphenated")
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['city', 'name']
        unique_together = [['city', 'slug']]
    
    def __str__(self):
        return f"{self.name}, {self.city.name}"