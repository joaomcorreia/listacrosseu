from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateWebsiteView.as_view(), name='create_website'),
    path('manage/', views.ManageWebsiteView.as_view(), name='manage_website'),
    path('edit/', views.EditWebsiteView.as_view(), name='edit_website'),
    path('domains/', views.DomainListView.as_view(), name='domain_list'),
    path('preview/', views.PreviewWebsiteView.as_view(), name='preview_website'),
    path('publish/', views.publish_website, name='publish_website'),
    path('unpublish/', views.unpublish_website, name='unpublish_website'),
    path('contact/', views.contact_form_submit, name='contact_form_submit'),
    # Public website display
    path('display/', views.display_website, name='display_website'),
    path('display/<str:subdomain>/', views.display_website, name='display_website_subdomain'),
]