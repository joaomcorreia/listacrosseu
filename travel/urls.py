from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.hybrid_home, name='hybrid_home'),
    path('guides/', views.article_list, name='article_list'),
    path('guide/<slug:slug>/', views.article_detail, name='article_detail'),
    path('track-view/<int:article_id>/', views.track_view, name='track_view'),
]