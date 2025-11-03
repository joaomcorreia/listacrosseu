from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('category/<slug:category_slug>/', views.BlogCategoryView.as_view(), name='category'),
    path('tag/<str:tag>/', views.BlogTagView.as_view(), name='tag'),
]