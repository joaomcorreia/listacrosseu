from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/', views.user_detail, name='user-detail'),
    path('set-language/', views.set_language_preference, name='set-language'),
]