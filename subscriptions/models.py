from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal
import uuid

User = get_user_model()


class SubscriptionPlan(models.Model):
    """Subscription plans with pricing and features"""
    
    PLAN_TYPES = [
        ('free', _('Free')),
        ('local', _('Local')),
        ('country', _('Country')),
        ('eu', _('EU')),
    ]
    
    BILLING_PERIODS = [
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    ]
    
    name = models.CharField(_('name'), max_length=100)
    plan_type = models.CharField(_('plan type'), max_length=20, choices=PLAN_TYPES, unique=True)
    description = models.TextField(_('description'))
    
    # Pricing
    monthly_price = models.DecimalField(_('monthly price'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    yearly_price = models.DecimalField(_('yearly price'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Features
    max_listings = models.PositiveIntegerField(_('max listings'), help_text=_('0 = unlimited'))
    can_create_website = models.BooleanField(_('can create website'), default=False)
    can_choose_domain = models.BooleanField(_('can choose domain'), default=False)
    can_upload_logo = models.BooleanField(_('can upload logo'), default=False)
    priority_support = models.BooleanField(_('priority support'), default=False)
    featured_listings = models.BooleanField(_('featured listings'), default=False)
    analytics_access = models.BooleanField(_('analytics access'), default=False)
    api_access = models.BooleanField(_('API access'), default=False)
    
    # Stripe integration
    stripe_monthly_price_id = models.CharField(_('Stripe monthly price ID'), max_length=100, blank=True)
    stripe_yearly_price_id = models.CharField(_('Stripe yearly price ID'), max_length=100, blank=True)
    
    # Settings
    is_active = models.BooleanField(_('is active'), default=True)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Subscription Plan')
        verbose_name_plural = _('Subscription Plans')
        ordering = ['sort_order', 'monthly_price']
    
    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"
    
    def get_price(self, billing_period='monthly'):
        """Get price for specific billing period"""
        if billing_period == 'yearly':
            return self.yearly_price
        return self.monthly_price
    
    def get_stripe_price_id(self, billing_period='monthly'):
        """Get Stripe price ID for specific billing period"""
        if billing_period == 'yearly':
            return self.stripe_yearly_price_id
        return self.stripe_monthly_price_id


class Subscription(models.Model):
    """User subscriptions"""
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('cancelled', _('Cancelled')),
        ('expired', _('Expired')),
        ('past_due', _('Past Due')),
        ('trialing', _('Trialing')),
    ]
    
    BILLING_PERIODS = [
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    
    # Billing
    billing_period = models.CharField(_('billing period'), max_length=20, choices=BILLING_PERIODS, default='monthly')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Dates
    start_date = models.DateTimeField(_('start date'), default=timezone.now)
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    current_period_start = models.DateTimeField(_('current period start'), default=timezone.now)
    current_period_end = models.DateTimeField(_('current period end'), null=True, blank=True)
    trial_end = models.DateTimeField(_('trial end'), null=True, blank=True)
    cancelled_at = models.DateTimeField(_('cancelled at'), null=True, blank=True)
    
    # Stripe integration
    stripe_subscription_id = models.CharField(_('Stripe subscription ID'), max_length=100, blank=True)
    stripe_customer_id = models.CharField(_('Stripe customer ID'), max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.full_name} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        if self.status != 'active':
            return False
        
        now = timezone.now()
        if self.end_date and self.end_date < now:
            return False
        
        if self.current_period_end and self.current_period_end < now:
            return False
        
        return True
    
    @property
    def is_trial(self):
        """Check if subscription is in trial period"""
        if not self.trial_end:
            return False
        return timezone.now() < self.trial_end
    
    @property
    def days_remaining(self):
        """Get days remaining in current period"""
        if not self.current_period_end:
            return None
        
        remaining = self.current_period_end - timezone.now()
        return max(0, remaining.days)
    
    def cancel(self, at_period_end=True):
        """Cancel subscription"""
        self.cancelled_at = timezone.now()
        if not at_period_end:
            self.status = 'cancelled'
            self.end_date = timezone.now()
        self.save()
    
    def reactivate(self):
        """Reactivate cancelled subscription"""
        self.status = 'active'
        self.cancelled_at = None
        self.end_date = None
        self.save()


class SubscriptionUsage(models.Model):
    """Track subscription usage (listings, API calls, etc.)"""
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage')
    
    # Usage metrics
    listings_used = models.PositiveIntegerField(_('listings used'), default=0)
    api_calls_used = models.PositiveIntegerField(_('API calls used'), default=0)
    storage_used = models.PositiveIntegerField(_('storage used (MB)'), default=0)
    
    # Period tracking
    period_start = models.DateTimeField(_('period start'))
    period_end = models.DateTimeField(_('period end'))
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Subscription Usage')
        verbose_name_plural = _('Subscription Usages')
        ordering = ['-period_start']
        unique_together = ['subscription', 'period_start']
    
    def __str__(self):
        return f"{self.subscription.user.full_name} - {self.period_start.strftime('%Y-%m')}"
    
    @property
    def listings_remaining(self):
        """Calculate remaining listings for current period"""
        max_listings = self.subscription.plan.max_listings
        if max_listings == 0:  # Unlimited
            return float('inf')
        return max(0, max_listings - self.listings_used)
    
    def can_create_listing(self):
        """Check if user can create another listing"""
        return self.listings_remaining > 0 or self.subscription.plan.max_listings == 0


class Invoice(models.Model):
    """Subscription invoices"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('open', _('Open')),
        ('paid', _('Paid')),
        ('void', _('Void')),
        ('uncollectible', _('Uncollectible')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    
    # Invoice details
    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Amounts
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    # Dates
    issue_date = models.DateTimeField(_('issue date'), default=timezone.now)
    due_date = models.DateTimeField(_('due date'), null=True, blank=True)
    paid_date = models.DateTimeField(_('paid date'), null=True, blank=True)
    
    # Stripe integration
    stripe_invoice_id = models.CharField(_('Stripe invoice ID'), max_length=100, blank=True)
    
    # Files
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.subscription.user.full_name}"
    
    @property
    def is_paid(self):
        return self.status == 'paid'
    
    @property
    def is_overdue(self):
        if not self.due_date or self.is_paid:
            return False
        return timezone.now() > self.due_date