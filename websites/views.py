from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.urls import reverse
from .models import Website, Domain, ContactSubmission


class CreateWebsiteView(LoginRequiredMixin, TemplateView):
    """Create a new website (EU plan only)"""
    template_name = 'websites/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user can create website
        if not request.user.can_create_website:
            messages.error(request, 'Website creation is only available for EU plan subscribers.')
            return redirect('subscription_plans')
        
        # Check if user already has a website
        if hasattr(request.user, 'website'):
            messages.info(request, 'You already have a website. You can edit it below.')
            return redirect('manage_website')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_domains'] = Domain.objects.filter(status='available')[:20]
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle website creation
        domain_id = request.POST.get('domain_id')
        title = request.POST.get('title', '')
        
        if not domain_id or not title:
            messages.error(request, 'Please provide all required information.')
            return self.get(request, *args, **kwargs)
        
        try:
            domain = Domain.objects.get(id=domain_id, status='available')
            
            # Create website
            website = Website.objects.create(
                user=request.user,
                domain=domain,
                title=title,
                tagline=request.POST.get('tagline', ''),
                description=request.POST.get('description', ''),
                theme=request.POST.get('theme', 'modern')
            )
            
            # Reserve domain
            domain.status = 'active'
            domain.user = request.user
            domain.save()
            
            messages.success(request, 'Website created successfully!')
            return redirect('manage_website')
            
        except Domain.DoesNotExist:
            messages.error(request, 'Selected domain is not available.')
            return self.get(request, *args, **kwargs)


class ManageWebsiteView(LoginRequiredMixin, TemplateView):
    """Manage existing website"""
    template_name = 'websites/manage.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'website'):
            messages.error(request, 'You don\'t have a website yet.')
            return redirect('create_website')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['website'] = self.request.user.website
        context['contact_submissions'] = ContactSubmission.objects.filter(
            website=self.request.user.website
        ).order_by('-created_at')[:10]
        return context


class EditWebsiteView(LoginRequiredMixin, UpdateView):
    """Edit website content and settings"""
    model = Website
    template_name = 'websites/edit.html'
    fields = [
        'title', 'tagline', 'description', 'theme', 'primary_color',
        'secondary_color', 'font_family', 'logo', 'favicon', 'hero_image',
        'about_section', 'services_section', 'contact_section',
        'meta_title', 'meta_description', 'keywords',
        'facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url',
        'enable_contact_form', 'google_analytics_id'
    ]
    
    def get_object(self):
        return self.request.user.website
    
    def get_success_url(self):
        messages.success(self.request, 'Website updated successfully!')
        return reverse('manage_website')


class DomainListView(LoginRequiredMixin, ListView):
    """List available domains"""
    model = Domain
    template_name = 'websites/domain_list.html'
    context_object_name = 'domains'
    
    def get_queryset(self):
        return Domain.objects.filter(status='available')


class PreviewWebsiteView(LoginRequiredMixin, TemplateView):
    """Preview website before publishing"""
    template_name = 'websites/preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'website'):
            context['website'] = self.request.user.website
        return context


@login_required
def publish_website(request):
    """Publish website"""
    if hasattr(request.user, 'website'):
        website = request.user.website
        website.publish()
        messages.success(request, f'Website published at {website.url}')
    else:
        messages.error(request, 'No website found.')
    
    return redirect('manage_website')


@login_required
def unpublish_website(request):
    """Unpublish website"""
    if hasattr(request.user, 'website'):
        website = request.user.website
        website.unpublish()
        messages.success(request, 'Website unpublished.')
    else:
        messages.error(request, 'No website found.')
    
    return redirect('manage_website')


def contact_form_submit(request):
    """Handle contact form submissions from user websites"""
    if request.method == 'POST' and hasattr(request, 'website'):
        website = request.website
        
        # Create contact submission
        submission = ContactSubmission.objects.create(
            website=website,
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', '')
        )
        
        # Update website contact submissions count
        website.contact_submissions += 1
        website.save(update_fields=['contact_submissions'])
        
        return JsonResponse({'success': True, 'message': 'Thank you for your message!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


def display_website(request, subdomain=None):
    """Public view to display user websites"""
    if subdomain:
        # Display specific website by subdomain
        domain_name = f"{subdomain}.listacross.eu"
        website = get_object_or_404(Website, domain__domain_name=domain_name, status='published')
    else:
        # For development, show any published website
        website = Website.objects.filter(status='published').first()
        if not website:
            raise Http404("No published websites found")
    
    context = {
        'website': website,
        'domain': website.domain,
        'show_business_listings': website.show_business_listings,
    }
    
    # Add business listings if enabled
    if website.show_business_listings and hasattr(website.user, 'businesses'):
        context['businesses'] = website.user.businesses.filter(status='active')[:10]
    
    return render(request, 'websites/display.html', context)