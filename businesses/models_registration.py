"""
Business Self-Registration System for ListAcross.eu
100% Legal - Business owners register themselves
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from businesses.models import Business, Category, City
import uuid
from PIL import Image
import os

User = get_user_model()

class BusinessRegistration(models.Model):
    """Pending business registration submissions"""
    
    VERIFICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('needs_info', 'Needs More Information'),
    ]
    
    # Unique identifier
    registration_id = models.UUIDField(default=uuid.uuid4, unique=True)
    
    # Business Information
    business_name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Location
    address = models.CharField(max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Contact Information
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits."
    )
    phone_number = models.CharField(validators=[phone_validator], max_length=17)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Business Owner Information
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    owner_phone = models.CharField(validators=[phone_validator], max_length=17)
    
    # Business Details
    opening_hours = models.JSONField(default=dict, blank=True)
    price_range = models.CharField(
        max_length=10,
        choices=[('$', 'Budget'), ('$$', 'Moderate'), ('$$$', 'Expensive'), ('$$$$', 'Very Expensive')],
        blank=True
    )
    
    # Verification
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS, 
        default='pending'
    )
    verification_notes = models.TextField(blank=True)
    
    # Business Documents (optional)
    business_license = models.FileField(upload_to='registrations/licenses/', blank=True, null=True)
    business_photos = models.JSONField(default=list, blank=True)  # Store photo paths
    
    # Verification Codes
    email_verification_code = models.CharField(max_length=6, blank=True)
    phone_verification_code = models.CharField(max_length=6, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Business Account (if they want premium features)
    wants_premium = models.BooleanField(default=False)
    premium_plan = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic Listing - Free'),
            ('enhanced', 'Enhanced Listing - €9.99/month'),
            ('premium', 'Premium Listing - €19.99/month'),
            ('featured', 'Featured Listing - €39.99/month'),
        ],
        default='basic'
    )
    
    class Meta:
        db_table = 'business_registrations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} - {self.city.name} ({self.verification_status})"
    
    def approve_registration(self, reviewed_by_user):
        """Convert registration to approved business listing"""
        from django.utils import timezone
        
        # Create the actual business
        business = Business.objects.create(
            name=self.business_name,
            description=self.description,
            address=self.address,
            city=self.city,
            phone_number=self.phone_number,
            email=self.email,
            website=self.website,
            latitude=self.latitude,
            longitude=self.longitude,
            category=self.category,
            opening_hours=self.opening_hours,
            price_range=self.price_range,
            verified=True,  # Mark as verified since owner submitted
            verification_method='owner_registration'
        )
        
        # Update registration status
        self.verification_status = 'verified'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by_user
        self.save()
        
        return business
    
    def generate_verification_codes(self):
        """Generate random 6-digit codes for email/phone verification"""
        import random
        self.email_verification_code = str(random.randint(100000, 999999))
        self.phone_verification_code = str(random.randint(100000, 999999))
        self.save()


class BusinessPhoto(models.Model):
    """Photos uploaded by business owners"""
    registration = models.ForeignKey(BusinessRegistration, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='registrations/photos/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'business_photos'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Compress image
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 1200:
                img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
                img.save(self.image.path, quality=85, optimize=True)


class BusinessClaim(models.Model):
    """For existing businesses that owners want to claim"""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    claimant_name = models.CharField(max_length=100)
    claimant_email = models.EmailField()
    claimant_phone = models.CharField(max_length=17)
    
    # Proof of ownership
    ownership_proof = models.FileField(upload_to='claims/proof/')
    verification_method = models.CharField(
        max_length=50,
        choices=[
            ('business_license', 'Business License'),
            ('utility_bill', 'Utility Bill'),
            ('lease_agreement', 'Lease Agreement'),
            ('tax_document', 'Tax Document'),
            ('other', 'Other Documentation'),
        ]
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'business_claims'