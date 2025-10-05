"""
Forms for Business Registration System
"""

from django import forms
from django.core.validators import RegexValidator
from .models import BusinessRegistration, BusinessPhoto, BusinessClaim
from .models import Category, City
import json

class BusinessRegistrationForm(forms.ModelForm):
    """Form for business owners to register their business"""
    
    # Additional fields for better UX
    confirm_email = forms.EmailField(
        label="Confirm Email",
        help_text="Please confirm your email address"
    )
    
    terms_accepted = forms.BooleanField(
        label="I accept the Terms of Service and Privacy Policy",
        required=True,
        error_messages={'required': 'You must accept the terms to continue.'}
    )
    
    data_consent = forms.BooleanField(
        label="I consent to my business information being displayed on ListAcross.eu",
        required=True,
        error_messages={'required': 'Business listing consent is required.'}
    )
    
    owner_verification = forms.BooleanField(
        label="I confirm that I am the owner or authorized representative of this business",
        required=True,
        error_messages={'required': 'Owner verification is required.'}
    )
    
    class Meta:
        model = BusinessRegistration
        fields = [
            'business_name', 'description', 'category', 'address', 'city', 
            'postal_code', 'phone_number', 'email', 'website', 
            'owner_name', 'owner_email', 'owner_phone', 'price_range',
            'wants_premium', 'premium_plan'
        ]
        
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your Business Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe your business, services, and what makes you special...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Street address'
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Postal Code'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+1234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'business@example.com'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://yourbusiness.com'
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Your full name'
            }),
            'owner_email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'your.email@example.com'
            }),
            'owner_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+1234567890'
            }),
            'price_range': forms.Select(attrs={'class': 'form-select'}),
            'premium_plan': forms.Select(attrs={'class': 'form-select'}),
        }
        
        help_texts = {
            'description': 'Tell potential customers about your business. What services do you offer? What makes you unique?',
            'phone_number': 'Include country code (e.g., +49 for Germany)',
            'website': 'Your business website (optional)',
            'price_range': 'Help customers understand your pricing level',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter categories to show only child categories (not parents)
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)
        
        # Group cities by country for better UX
        self.fields['city'].queryset = City.objects.select_related('country').order_by('country__name', 'name')
        
        # Make premium plan conditional
        self.fields['premium_plan'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Email addresses don't match.")
        
        return cleaned_data


class BusinessPhotoForm(forms.ModelForm):
    """Form for uploading business photos"""
    
    class Meta:
        model = BusinessPhoto
        fields = ['image', 'caption', 'is_primary']
        
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Photo caption (optional)'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        help_texts = {
            'image': 'Upload high-quality photos of your business (max 5MB each)',
            'is_primary': 'Check this to make this your main business photo',
        }


class BusinessHoursForm(forms.Form):
    """Form for setting business hours"""
    
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for day_code, day_name in self.DAYS:
            self.fields[f'{day_code}_open'] = forms.TimeField(
                required=False,
                widget=forms.TimeInput(attrs={
                    'class': 'form-control', 
                    'type': 'time'
                }),
                label=f'{day_name} Open'
            )
            self.fields[f'{day_code}_close'] = forms.TimeField(
                required=False,
                widget=forms.TimeInput(attrs={
                    'class': 'form-control', 
                    'type': 'time'
                }),
                label=f'{day_name} Close'
            )
            self.fields[f'{day_code}_closed'] = forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-check-input'
                }),
                label=f'{day_name} Closed'
            )
    
    def get_hours_json(self):
        """Convert form data to JSON format for storage"""
        hours = {}
        for day_code, day_name in self.DAYS:
            if self.cleaned_data.get(f'{day_code}_closed'):
                hours[day_code] = {'closed': True}
            else:
                open_time = self.cleaned_data.get(f'{day_code}_open')
                close_time = self.cleaned_data.get(f'{day_code}_close')
                if open_time and close_time:
                    hours[day_code] = {
                        'open': open_time.strftime('%H:%M'),
                        'close': close_time.strftime('%H:%M'),
                        'closed': False
                    }
        return hours


class BusinessClaimForm(forms.ModelForm):
    """Form for claiming existing businesses"""
    
    terms_accepted = forms.BooleanField(
        label="I accept the Terms of Service",
        required=True
    )
    
    ownership_confirmation = forms.BooleanField(
        label="I confirm that I am the legal owner of this business",
        required=True
    )
    
    class Meta:
        model = BusinessClaim
        fields = [
            'claimant_name', 'claimant_email', 'claimant_phone',
            'ownership_proof', 'verification_method'
        ]
        
        widgets = {
            'claimant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'claimant_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'claimant_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'ownership_proof': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'verification_method': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
        help_texts = {
            'ownership_proof': 'Upload business license, utility bill, lease agreement, or tax document',
            'verification_method': 'Select the type of document you are uploading',
        }


class QuickSearchForm(forms.Form):
    """Quick search form for homepage"""
    
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'What are you looking for? (restaurants, hotels, shops...)',
            'autocomplete': 'off'
        }),
        required=False
    )
    
    city = forms.ModelChoiceField(
        queryset=City.objects.select_related('country').order_by('country__name', 'name'),
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg'
        }),
        required=False,
        empty_label="Select City"
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=False),
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg'
        }),
        required=False,
        empty_label="All Categories"
    )