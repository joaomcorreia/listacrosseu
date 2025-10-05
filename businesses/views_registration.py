"""
Views for Business Registration System
100% Legal - Business owners register themselves
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.conf import settings
from .models import BusinessRegistration, BusinessPhoto, Business, Category, City
from .forms_registration import (
    BusinessRegistrationForm, BusinessPhotoForm, 
    BusinessHoursForm, BusinessClaimForm, QuickSearchForm
)
import random
from django.utils import timezone


def register_business(request):
    """Business registration page"""
    
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST)
        hours_form = BusinessHoursForm(request.POST)
        
        if form.is_valid() and hours_form.is_valid():
            registration = form.save(commit=False)
            
            # Add opening hours
            registration.opening_hours = hours_form.get_hours_json()
            
            # Generate verification codes
            registration.generate_verification_codes()
            registration.save()
            
            # Send verification email
            send_verification_email(registration)
            
            messages.success(request, 
                f'Thank you! Your business registration has been submitted. '
                f'Please check your email for verification instructions.'
            )
            
            return redirect('verify_registration', registration_id=registration.registration_id)
        
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = BusinessRegistrationForm()
        hours_form = BusinessHoursForm()
    
    context = {
        'form': form,
        'hours_form': hours_form,
        'categories': Category.objects.filter(parent__isnull=False).order_by('name'),
        'cities': City.objects.select_related('country').order_by('country__name', 'name'),
    }
    
    return render(request, 'businesses/register.html', context)


def verify_registration(request, registration_id):
    """Email verification page"""
    
    registration = get_object_or_404(BusinessRegistration, registration_id=registration_id)
    
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code', '').strip()
        
        if verification_code == registration.email_verification_code:
            registration.email_verified = True
            registration.save()
            
            messages.success(request, 
                'Email verified successfully! Your registration is now under review.'
            )
            
            return redirect('registration_status', registration_id=registration_id)
        
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
    
    context = {
        'registration': registration,
    }
    
    return render(request, 'businesses/verify.html', context)


def registration_status(request, registration_id):
    """Check registration status"""
    
    registration = get_object_or_404(BusinessRegistration, registration_id=registration_id)
    
    context = {
        'registration': registration,
    }
    
    return render(request, 'businesses/status.html', context)


def business_claim(request, business_id):
    """Claim existing business"""
    
    business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        form = BusinessClaimForm(request.POST, request.FILES)
        
        if form.is_valid():
            claim = form.save(commit=False)
            claim.business = business
            claim.save()
            
            messages.success(request, 
                'Your claim has been submitted for review. '
                'You will be contacted within 2-3 business days.'
            )
            
            return redirect('business_detail', business_id=business.id)
    
    else:
        form = BusinessClaimForm()
    
    context = {
        'business': business,
        'form': form,
    }
    
    return render(request, 'businesses/claim.html', context)


def homepage(request):
    """Enhanced homepage with search"""
    
    # Get search parameters
    search_form = QuickSearchForm(request.GET or None)
    query = request.GET.get('query', '').strip()
    city_id = request.GET.get('city')
    category_id = request.GET.get('category')
    
    # Base queryset
    businesses = Business.objects.filter(verified=True).select_related('city', 'category')
    
    # Apply filters
    if query:
        businesses = businesses.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    if city_id:
        businesses = businesses.filter(city_id=city_id)
    
    if category_id:
        businesses = businesses.filter(
            Q(category_id=category_id) |
            Q(category__parent_id=category_id)
        )
    
    # Pagination
    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses_page = paginator.get_page(page)
    
    # Stats for display
    stats = {
        'total_businesses': Business.objects.filter(verified=True).count(),
        'total_cities': City.objects.count(),
        'total_categories': Category.objects.filter(parent__isnull=False).count(),
    }
    
    # Featured categories
    featured_categories = Category.objects.filter(
        parent__isnull=False
    ).annotate(
        business_count=Count('businesses')
    ).order_by('-business_count')[:6]
    
    # Popular cities
    popular_cities = City.objects.annotate(
        business_count=Count('businesses')
    ).order_by('-business_count')[:8]
    
    context = {
        'search_form': search_form,
        'businesses': businesses_page,
        'stats': stats,
        'featured_categories': featured_categories,
        'popular_cities': popular_cities,
        'query': query,
        'selected_city_id': city_id,
        'selected_category_id': category_id,
    }
    
    return render(request, 'businesses/homepage.html', context)


@require_http_methods(["POST"])
def resend_verification(request, registration_id):
    """Resend verification email"""
    
    registration = get_object_or_404(BusinessRegistration, registration_id=registration_id)
    
    if not registration.email_verified:
        # Generate new code
        registration.generate_verification_codes()
        
        # Send new email
        send_verification_email(registration)
        
        return JsonResponse({
            'success': True,
            'message': 'Verification email sent successfully!'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Email already verified.'
    })


def send_verification_email(registration):
    """Send verification email to business owner"""
    
    subject = f'Verify your business registration - ListAcross.eu'
    
    message = f"""
    Hello {registration.owner_name},
    
    Thank you for registering your business "{registration.business_name}" on ListAcross.eu!
    
    To complete your registration, please verify your email address by using this code:
    
    Verification Code: {registration.email_verification_code}
    
    Or click this link: {settings.SITE_URL}/verify/{registration.registration_id}/
    
    Your business will be reviewed and published within 24-48 hours.
    
    Questions? Reply to this email or contact us at support@listacross.eu
    
    Best regards,
    The ListAcross.eu Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.owner_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")


def business_success_stories(request):
    """Success stories from business owners"""
    
    # Sample success stories - replace with real testimonials
    stories = [
        {
            'business_name': 'Café Mozart',
            'owner': 'Maria Schmidt',
            'city': 'Vienna',
            'story': 'Listing my café on ListAcross.eu increased our international visitors by 40%! The platform makes it so easy to reach tourists across Europe.',
            'rating': 5,
        },
        {
            'business_name': 'Villa Rental Tuscany',
            'owner': 'Giuseppe Rossi',
            'city': 'Florence',
            'story': 'As a small family business, ListAcross.eu gave us exposure we could never afford elsewhere. Bookings have doubled since joining.',
            'rating': 5,
        },
    ]
    
    context = {
        'stories': stories,
        'stats': {
            'businesses_joined_this_month': 156,
            'average_rating_increase': '4.2 stars',
            'customer_increase': '35%',
        }
    }
    
    return render(request, 'businesses/success_stories.html', context)


def pricing_plans(request):
    """Pricing page for business owners"""
    
    plans = [
        {
            'name': 'Basic Listing',
            'price': 'Free',
            'features': [
                'Basic business information',
                'Contact details',
                'Opening hours',
                'Customer reviews',
                'Mobile-friendly listing',
            ],
            'popular': False,
        },
        {
            'name': 'Enhanced Listing',
            'price': '€9.99/month',
            'features': [
                'Everything in Basic',
                'Photo gallery (up to 10 photos)',
                'Detailed description',
                'Social media links',
                'Priority in search results',
                'Basic analytics dashboard',
            ],
            'popular': True,
        },
        {
            'name': 'Premium Listing',
            'price': '€19.99/month',
            'features': [
                'Everything in Enhanced',
                'Unlimited photos',
                'Video showcase',
                'Featured badge',
                'Top search placement',
                'Advanced analytics',
                'Direct booking integration',
            ],
            'popular': False,
        },
        {
            'name': 'Featured Business',
            'price': '€39.99/month',
            'features': [
                'Everything in Premium',
                'Homepage featured placement',
                'Category page highlights',
                'Promotional banner space',
                'Dedicated account manager',
                'Custom marketing campaigns',
                'API access for integrations',
            ],
            'popular': False,
        },
    ]
    
    context = {
        'plans': plans,
    }
    
    return render(request, 'businesses/pricing.html', context)