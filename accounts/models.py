from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    arabic_on_dashboard = models.BooleanField(
        default=False,
        verbose_name=_('Arabic on Dashboard'),
        help_text=_('Enable Arabic language support on the dashboard')
    )
    arabic_on_website = models.BooleanField(
        default=False,
        verbose_name=_('Arabic on Website'),
        help_text=_('Enable Arabic language support on the public website')
    )
    preferred_language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', _('English')),
            ('fr', _('French')),
            ('nl', _('Dutch')),
            ('pt', _('Portuguese')),
            ('de', _('German')),
            ('es', _('Spanish')),
            ('ar', _('Arabic')),
        ],
        verbose_name=_('Preferred Language'),
        help_text=_('User\'s preferred language for the interface')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_effective_language(self):
        """Get the effective language based on user preferences"""
        if self.arabic_on_dashboard or self.arabic_on_website:
            return 'ar'
        return self.preferred_language