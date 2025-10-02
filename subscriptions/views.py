from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from .models import SubscriptionPlan, Subscription


class SubscriptionPlanListView(ListView):
    """List all available subscription plans"""
    model = SubscriptionPlan
    template_name = 'subscriptions/plan_list.html'
    context_object_name = 'plans'
    
    def get_queryset(self):
        return SubscriptionPlan.objects.filter(is_active=True).order_by('sort_order')


class SubscribeView(LoginRequiredMixin, TemplateView):
    """Subscribe to a plan"""
    template_name = 'subscriptions/subscribe.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_type = kwargs.get('plan_type')
        try:
            context['plan'] = SubscriptionPlan.objects.get(plan_type=plan_type, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            context['plan'] = None
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle subscription creation
        plan_type = kwargs.get('plan_type')
        
        try:
            plan = SubscriptionPlan.objects.get(plan_type=plan_type, is_active=True)
            
            # Create or update subscription
            subscription, created = Subscription.objects.get_or_create(
                user=request.user,
                defaults={
                    'plan': plan,
                    'status': 'active'
                }
            )
            
            if not created:
                # Update existing subscription
                subscription.plan = plan
                subscription.status = 'active'
                subscription.save()
            
            # Update user subscription type
            request.user.subscription_type = plan_type
            request.user.subscription_active = True
            request.user.save()
            
            messages.success(request, f'Successfully subscribed to {plan.name}!')
            return redirect('manage_subscription')
            
        except SubscriptionPlan.DoesNotExist:
            messages.error(request, 'Invalid subscription plan.')
            return redirect('subscription_plans')


@login_required
def manage_subscription_view(request):
    """Manage current subscription"""
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None
    
    context = {
        'subscription': subscription,
        'available_plans': SubscriptionPlan.objects.filter(is_active=True)
    }
    
    return render(request, 'subscriptions/manage.html', context)


class ManageSubscriptionView(LoginRequiredMixin, TemplateView):
    """Manage subscription view"""
    template_name = 'subscriptions/manage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['subscription'] = Subscription.objects.get(user=self.request.user)
        except Subscription.DoesNotExist:
            context['subscription'] = None
        
        context['available_plans'] = SubscriptionPlan.objects.filter(is_active=True)
        return context


class CancelSubscriptionView(LoginRequiredMixin, TemplateView):
    """Cancel subscription"""
    template_name = 'subscriptions/cancel.html'
    
    def post(self, request, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(user=request.user)
            subscription.cancel()
            
            # Update user
            request.user.subscription_type = 'free'
            request.user.subscription_active = False
            request.user.save()
            
            messages.success(request, 'Subscription cancelled successfully.')
            
        except Subscription.DoesNotExist:
            messages.error(request, 'No active subscription found.')
        
        return redirect('subscription_plans')