from django.contrib import admin
from django.utils.html import format_html


# Since payments app doesn't have its own models, we'll create a custom admin view
# for payment-related functionality and monitoring

class PaymentAdminSite(admin.AdminSite):
    """Custom admin site for payment management"""
    site_header = 'Payment Administration'
    site_title = 'Payment Admin'
    index_title = 'Payment Management'


# Create custom admin views for payment monitoring
class PaymentDashboard:
    """Payment dashboard functionality"""
    
    @staticmethod
    def get_payment_stats():
        """Get payment statistics"""
        try:
            from django.contrib.auth import get_user_model
            from subscriptions.models import SubscriptionPlan
            
            User = get_user_model()
            
            stats = {
                'total_subscribers': User.objects.exclude(
                    subscription_plan__name__icontains='free'
                ).count(),
                'free_users': User.objects.filter(
                    subscription_plan__name__icontains='free'
                ).count(),
            }
            
            # Get subscription breakdown
            for plan in SubscriptionPlan.objects.all():
                stats[f'{plan.name.lower()}_subscribers'] = User.objects.filter(
                    subscription_plan=plan
                ).count()
            
            return stats
        except:
            return {}


# Register custom admin functionality
def register_payment_admin(admin_site=None):
    """Register payment-related admin functionality"""
    if admin_site is None:
        admin_site = admin.site
    
    # TODO: Add payment dashboard to admin index when template is created
    # admin_site.index_template = 'admin/payment_index.html'
    pass


# Auto-register when imported  
register_payment_admin()