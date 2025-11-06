from django.urls import path
from . import views

app_name = 'blog_ai'

urlpatterns = [
    path('outline/', views.generate_outline, name='generate_outline'),
    path('draft/', views.generate_draft, name='generate_draft'),
    path('seo/', views.generate_seo, name='generate_seo'),
    path('translate/', views.translate_article, name='translate_article'),
    path('status/', views.ai_status, name='ai_status'),
]