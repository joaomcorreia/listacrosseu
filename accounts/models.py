from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    """Custom user model with additional fields for business owners"""
    
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    company_name = models.CharField(_('company name'), max_length=200, blank=True)
    
    # Profile fields
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    personal_website = models.URLField(_('personal website'), blank=True)
    
    # Address fields
    address = models.CharField(_('address'), max_length=200, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    
    # Subscription fields
    subscription_type = models.CharField(
        _('subscription type'),
        max_length=20,
        choices=[
            ('free', _('Free')),
            ('local', _('Local (€29/month)')),
            ('country', _('Country (€79/month)')),
            ('eu', _('EU (€199/month)')),
        ],
        default='free'
    )
    subscription_active = models.BooleanField(_('subscription active'), default=True)
    subscription_expires = models.DateTimeField(_('subscription expires'), null=True, blank=True)
    
    # Verification fields
    is_verified = models.BooleanField(_('is verified'), default=False)
    verification_documents = models.FileField(
        upload_to='verification_docs/',
        blank=True,
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    last_login_ip = models.GenericIPAddressField(_('last login IP'), null=True, blank=True)
    
    # Marketing preferences
    marketing_emails = models.BooleanField(_('marketing emails'), default=True)
    newsletter = models.BooleanField(_('newsletter'), default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def has_active_subscription(self):
        """Check if user has an active paid subscription"""
        if self.subscription_type == 'free':
            return False
        return self.subscription_active and (
            self.subscription_expires is None or 
            self.subscription_expires > timezone.now()
        )
    
    @property
    def can_create_website(self):
        """Check if user can create a custom website (EU plan only)"""
        return self.subscription_type == 'eu' and self.has_active_subscription
    
    def get_subscription_display_name(self):
        """Get human-readable subscription name"""
        subscription_names = {
            'free': 'Free Plan',
            'local': 'Local Plan (€29/month)',
            'country': 'Country Plan (€79/month)',
            'eu': 'EU Plan (€199/month)',
        }
        return subscription_names.get(self.subscription_type, 'Unknown Plan')