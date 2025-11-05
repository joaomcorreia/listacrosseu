from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Plan Name'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    currency = models.CharField(max_length=3, default='EUR', verbose_name=_('Currency'))
    billing_period = models.CharField(
        max_length=20,
        choices=[
            ('monthly', _('Monthly')),
            ('yearly', _('Yearly')),
        ],
        default='monthly',
        verbose_name=_('Billing Period')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Subscription Plan')
        verbose_name_plural = _('Subscription Plans')
    
    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}/{self.billing_period}"


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name=_('Plan'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    auto_renew = models.BooleanField(default=True, verbose_name=_('Auto Renew'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('User Subscription')
        verbose_name_plural = _('User Subscriptions')
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, verbose_name=_('Subscription'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    currency = models.CharField(max_length=3, default='EUR', verbose_name=_('Currency'))
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('paid', _('Paid')),
            ('failed', _('Failed')),
            ('refunded', _('Refunded')),
        ],
        default='pending',
        verbose_name=_('Status')
    )
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name=_('Invoice Number'))
    due_date = models.DateTimeField(verbose_name=_('Due Date'))
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Paid At'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.username}"