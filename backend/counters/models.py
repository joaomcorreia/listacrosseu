from django.db import models
from catalog.models import Category
from geo.models import Country, City, Town


class CategoryCountry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    business_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = [['category', 'country']]
        verbose_name = "Category Country Count"
        verbose_name_plural = "Category Country Counts"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['country']),
            models.Index(fields=['business_count']),
        ]
    
    def __str__(self):
        return f"{self.category.slug} in {self.country.code}: {self.business_count}"


class CategoryCountryCity(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    business_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = [['category', 'country', 'city']]
        verbose_name = "Category Country City Count"
        verbose_name_plural = "Category Country City Counts"
        indexes = [
            models.Index(fields=['category', 'country']),
            models.Index(fields=['city']),
            models.Index(fields=['business_count']),
        ]
    
    def __str__(self):
        return f"{self.category.slug} in {self.city.name}, {self.country.code}: {self.business_count}"


class CategoryCityTown(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    business_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = [['category', 'city', 'town']]
        verbose_name = "Category City Town Count"
        verbose_name_plural = "Category City Town Counts"
        indexes = [
            models.Index(fields=['category', 'city']),
            models.Index(fields=['town']),
            models.Index(fields=['business_count']),
        ]
    
    def __str__(self):
        return f"{self.category.slug} in {self.town.name}, {self.city.name}: {self.business_count}"


class CounterRebuildLog(models.Model):
    """Track when counters were last rebuilt"""
    rebuilt_at = models.DateTimeField(auto_now_add=True)
    rebuild_type = models.CharField(max_length=50, default='full')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-rebuilt_at']
    
    def __str__(self):
        return f"Counter rebuild: {self.rebuild_type} at {self.rebuilt_at}"