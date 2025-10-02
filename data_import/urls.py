from django.urls import path
from . import views

urlpatterns = [
    path('', views.ImportDashboardView.as_view(), name='import_dashboard'),
    path('create/', views.CreateImportView.as_view(), name='create_import'),
    path('jobs/', views.ImportJobListView.as_view(), name='import_job_list'),
    path('jobs/<int:pk>/', views.ImportJobDetailView.as_view(), name='import_job_detail'),
    path('jobs/<int:job_id>/status/', views.import_job_status, name='import_job_status'),
    path('jobs/<int:job_id>/cancel/', views.cancel_import_job, name='cancel_import_job'),
    path('jobs/<int:job_id>/delete/', views.delete_import_job, name='delete_import_job'),
    path('mappings/create/', views.CreateMappingView.as_view(), name='create_mapping'),
    path('download-template/', views.download_template, name='download_template'),
]