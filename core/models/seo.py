from django.db import models

class SEOMixin(models.Model):
    """
    Abstract model to add SEO fields to any model.
    Provides meta title, description, canonical URL, robots, and Open Graph fields.
    """
    meta_title = models.CharField(
        "Meta Title", 
        max_length=70, 
        blank=True,
        help_text="Recommended: 50-60 characters. This appears as the clickable headline in search results."
    )
    meta_description = models.CharField(
        "Meta Description", 
        max_length=160, 
        blank=True,
        help_text="Recommended: 120-160 characters. This appears as the snippet under the title in search results."
    )
    canonical_url = models.URLField(
        "Canonical URL", 
        blank=True,
        help_text="Optional. Use to specify the preferred URL for this page to prevent duplicate content issues."
    )
    robots = models.CharField(
        "Robots", 
        max_length=50, 
        blank=True, 
        default="index,follow",
        help_text="Controls how search engines crawl this page. Common values: index,follow | noindex,nofollow | index,nofollow"
    )
    og_title = models.CharField(
        "Open Graph Title", 
        max_length=120, 
        blank=True,
        help_text="Title when shared on social media. Falls back to meta_title if empty."
    )
    og_description = models.CharField(
        "Open Graph Description", 
        max_length=200, 
        blank=True,
        help_text="Description when shared on social media. Falls back to meta_description if empty."
    )
    og_image = models.URLField(
        "Open Graph Image", 
        blank=True,
        help_text="Image when shared on social media. Recommended size: 1200x630px."
    )

    class Meta:
        abstract = True

    def get_meta_title(self):
        """Get meta title with fallback to model's title field if available."""
        if self.meta_title:
            return self.meta_title
        if hasattr(self, 'title'):
            return self.title
        if hasattr(self, 'name'):
            return self.name
        return ""

    def get_meta_description(self):
        """Get meta description with fallback to model's description field if available."""
        if self.meta_description:
            return self.meta_description
        if hasattr(self, 'description'):
            return self.description[:160]
        if hasattr(self, 'excerpt'):
            return self.excerpt[:160]
        return ""

    def get_og_title(self):
        """Get Open Graph title with fallback to meta title."""
        return self.og_title or self.get_meta_title()

    def get_og_description(self):
        """Get Open Graph description with fallback to meta description."""
        return self.og_description or self.get_meta_description()