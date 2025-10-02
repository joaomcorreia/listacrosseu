from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.SubscriptionPlanListView.as_view(), name='subscription_plans'),
    path('subscribe/<str:plan_type>/', views.SubscribeView.as_view(), name='subscribe'),
    path('manage/', views.ManageSubscriptionView.as_view(), name='manage_subscription'),
    path('cancel/', views.CancelSubscriptionView.as_view(), name='cancel_subscription'),
]