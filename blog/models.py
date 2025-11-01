from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from common.seo import SeoFieldsMixin
from django.urls import reverse
from plans.models import VisibilityProfile
import os

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class Post(SeoFieldsMixin):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("nl", "Dutch"),
        ("fr", "French"),
        ("es", "Spanish"),
        ("pt", "Portuguese"),
        ("de", "German"),
        ("it", "Italian"),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Brief description for cards and previews")
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blog/images/", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Related posts (many-to-many for flexible relationships)
    related_posts = models.ManyToManyField("self", blank=True, symmetrical=False)
    visibility = models.ForeignKey(VisibilityProfile, on_delete=models.PROTECT, null=True, blank=True)
    
    class Meta:
        unique_together = [["slug", "language"]]
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["language", "is_published"]),
            models.Index(fields=["category", "is_published"]),
            models.Index(fields=["is_featured", "is_published"]),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"lang": self.language, "slug": self.slug})
    
    def get_featured_image_url(self):
        if self.featured_image:
            return self.featured_image.url
        return None
    
    def get_related_posts(self, limit=3):
        """Get related posts for the card slider"""
        related = self.related_posts.filter(is_published=True, language=self.language)[:limit]
        if related.count() < limit and self.category:
            # Fill remaining slots with posts from same category
            category_posts = Post.objects.filter(
                category=self.category,
                is_published=True,
                language=self.language
            ).exclude(id=self.id).exclude(id__in=related.values_list("id", flat=True))[:limit - related.count()]
            related = list(related) + list(category_posts)
        return related
    
    def list_weight(self):
        """Calculate the weight for list ordering based on plan and featured status"""
        base = 0
        if self.visibility and self.visibility.plan:
            base += self.visibility.plan.priority_weight
        if self.visibility and self.visibility.featured:
            base += self.visibility.featured_weight
        return base
