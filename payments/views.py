from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import stripe

try:
    from subscriptions.models import SubscriptionPlan
except ImportError:
    SubscriptionPlan = None

# Configure Stripe
if hasattr(settings, 'STRIPE_SECRET_KEY'):
    stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(LoginRequiredMixin, TemplateView):
    """Handle payment processing"""
    template_name = 'payments/payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get plan from URL or request
        plan_id = self.request.GET.get('plan_id') or self.kwargs.get('plan_id')
        
        if plan_id and SubscriptionPlan:
            try:
                plan = SubscriptionPlan.objects.get(id=plan_id)
                context['plan'] = plan
                context['stripe_public_key'] = getattr(settings, 'STRIPE_PUBLIC_KEY', '')
            except SubscriptionPlan.DoesNotExist:
                messages.error(self.request, 'Invalid subscription plan.')
        
        return context


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    """Payment success page"""
    template_name = 'payments/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get session info
        session_id = self.request.GET.get('session_id')
        if session_id and hasattr(settings, 'STRIPE_SECRET_KEY'):
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                context['session'] = session
            except:
                pass
        
        return context


class PaymentCancelView(TemplateView):
    """Payment cancelled page"""
    template_name = 'payments/cancel.html'


@login_required
def create_checkout_session(request):
    """Create Stripe checkout session"""
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        
        if not plan_id or not SubscriptionPlan:
            return JsonResponse({'error': 'Invalid plan'}, status=400)
        
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
            
            # Create Stripe checkout session
            if hasattr(settings, 'STRIPE_SECRET_KEY'):
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': plan.name,
                                'description': plan.description,
                            },
                            'unit_amount': int(plan.price * 100),  # Convert to cents
                            'recurring': {
                                'interval': 'month',
                            },
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url=request.build_absolute_uri('/payments/success/?session_id={CHECKOUT_SESSION_ID}'),
                    cancel_url=request.build_absolute_uri('/payments/cancel/'),
                    customer_email=request.user.email,
                    metadata={
                        'user_id': request.user.id,
                        'plan_id': plan.id,
                    }
                )
                
                return JsonResponse({'checkout_url': session.url})
            else:
                return JsonResponse({'error': 'Payment system not configured'}, status=500)
                
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'error': 'Plan not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    if not hasattr(settings, 'STRIPE_WEBHOOK_SECRET'):
        return JsonResponse({'error': 'Webhook not configured'}, status=500)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_successful_subscription_payment(invoice)
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_failed_payment(invoice)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)
    
    return JsonResponse({'status': 'success'})


def handle_successful_payment(session):
    """Handle successful payment from Stripe"""
    try:
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        
        if SubscriptionPlan:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(id=user_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)
            
            # Update user subscription
            user.subscription_plan = plan
            user.stripe_customer_id = session['customer']
            user.save()
            
    except Exception as e:
        print(f"Error handling successful payment: {e}")


def handle_successful_subscription_payment(invoice):
    """Handle successful subscription payment"""
    try:
        customer_id = invoice['customer']
        
        if SubscriptionPlan:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(stripe_customer_id=customer_id)
            # Update subscription status if needed
            
    except Exception as e:
        print(f"Error handling subscription payment: {e}")


def handle_failed_payment(invoice):
    """Handle failed payment"""
    try:
        customer_id = invoice['customer']
        
        if SubscriptionPlan:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(stripe_customer_id=customer_id)
            # Handle failed payment (send email, update status, etc.)
            
    except Exception as e:
        print(f"Error handling failed payment: {e}")


def handle_subscription_cancelled(subscription):
    """Handle subscription cancellation"""
    try:
        customer_id = subscription['customer']
        
        if SubscriptionPlan:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(stripe_customer_id=customer_id)
            # Reset to free plan
            free_plan = SubscriptionPlan.objects.filter(name__icontains='free').first()
            if free_plan:
                user.subscription_plan = free_plan
                user.save()
                
    except Exception as e:
        print(f"Error handling subscription cancellation: {e}")