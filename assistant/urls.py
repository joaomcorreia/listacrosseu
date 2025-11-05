from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    path('chat/', views.assistant_chat, name='chat'),
    path('test/', views.assistant_test, name='test'),
    path('languages/', views.assistant_languages, name='languages'),
]