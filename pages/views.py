from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import JsonResponse


def home(request):
    """Home page view"""
    context = {
        'title': _('Welcome to ListAcross EU'),
        'description': _('Find the best businesses across Europe'),
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """About page view"""
    context = {
        'title': _('About Us'),
        'description': _('Learn more about ListAcross EU'),
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        # Handle contact form submission
        return JsonResponse({'status': 'success', 'message': _('Message sent successfully')})
    
    context = {
        'title': _('Contact Us'),
        'description': _('Get in touch with us'),
    }
    return render(request, 'pages/contact.html', context)