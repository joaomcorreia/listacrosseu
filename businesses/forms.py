from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import Business, City, Category
import json


class BusinessForm(forms.ModelForm):
    """Enhanced business form with duplicate prevention"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes for better styling
        self.fields['name'].widget.attrs.update({
            'class': 'vTextField duplicate-check-field',
            'data-field': 'name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'vTextField duplicate-check-field',
            'data-field': 'email'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'vTextField duplicate-check-field',
            'data-field': 'phone'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'duplicate-check-field',
            'data-field': 'city'
        })
        
        # Add help text for duplicate prevention
        self.fields['name'].help_text = format_html(
            '<span class="duplicate-status" id="name-status"></span>'
            'Business name will be checked for duplicates in the selected city.'
        )
        self.fields['email'].help_text = format_html(
            '<span class="duplicate-status" id="email-status"></span>'
            'Email will be checked for duplicates in the selected city.'
        )
        self.fields['phone'].help_text = format_html(
            '<span class="duplicate-status" id="phone-status"></span>'
            'Phone will be checked for duplicates in the selected city.'
        )

    class Meta:
        model = Business
        fields = '__all__'
        
    def clean(self):
        """Enhanced validation with duplicate checking"""
        cleaned_data = super().clean()
        
        name = cleaned_data.get('name')
        city = cleaned_data.get('city')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        if name and city:
            # Check for potential duplicates
            exclude_id = self.instance.pk if self.instance else None
            issues = Business.check_potential_duplicate(
                name=name,
                city=city, 
                email=email,
                phone=phone,
                exclude_id=exclude_id
            )
            
            if issues:
                error_message = "Potential duplicate detected! " + "; ".join(issues)
                raise ValidationError(error_message)
        
        return cleaned_data
        
    def clean_name(self):
        """Validate and normalize business name"""
        name = self.cleaned_data.get('name')
        if name:
            # Use the model's normalization method
            temp_business = Business()
            name = temp_business.normalize_business_name(name)
        return name


class DuplicateCheckForm(forms.Form):
    """Form for real-time duplicate checking via AJAX"""
    name = forms.CharField(max_length=200, required=False)
    city_id = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, required=False)
    exclude_id = forms.CharField(required=False)  # UUID as string
    
    def check_duplicates(self):
        """Check for duplicates and return formatted response"""
        if not self.is_valid():
            return {'error': 'Invalid form data'}
            
        name = self.cleaned_data.get('name')
        city_id = self.cleaned_data.get('city_id')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        exclude_id = self.cleaned_data.get('exclude_id')
        
        if not (name or email or phone) or not city_id:
            return {'status': 'incomplete', 'message': 'Enter business details to check for duplicates'}
            
        try:
            city = City.objects.get(pk=city_id)
        except City.DoesNotExist:
            return {'error': 'Invalid city selected'}
            
        # Check for duplicates
        issues = Business.check_potential_duplicate(
            name=name,
            city=city,
            email=email, 
            phone=phone,
            exclude_id=exclude_id
        )
        
        if issues:
            return {
                'status': 'duplicates_found',
                'message': 'Potential duplicates detected',
                'issues': issues,
                'severity': 'warning'
            }
        else:
            return {
                'status': 'no_duplicates',
                'message': 'No duplicates detected',
                'severity': 'success'
            }


class BulkImportForm(forms.Form):
    """Form for bulk import with duplicate prevention"""
    
    IMPORT_MODES = [
        ('skip', 'Skip Duplicates'),
        ('update', 'Update Existing'), 
        ('create_all', 'Create All (Allow Duplicates)'),
        ('abort', 'Abort on First Duplicate'),
    ]
    
    csv_file = forms.FileField(
        help_text="CSV file with business data. Required columns: name, email, city, category"
    )
    import_mode = forms.ChoiceField(
        choices=IMPORT_MODES,
        initial='skip',
        help_text="How to handle duplicate businesses during import"
    )
    check_duplicates = forms.BooleanField(
        initial=True,
        required=False,
        help_text="Perform duplicate checking (recommended)"
    )
    
    def clean_csv_file(self):
        """Validate CSV file"""
        csv_file = self.cleaned_data['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            raise ValidationError("File must be a CSV file")
            
        # Check file size (max 10MB)
        if csv_file.size > 10 * 1024 * 1024:
            raise ValidationError("File too large. Maximum size is 10MB")
            
        return csv_file