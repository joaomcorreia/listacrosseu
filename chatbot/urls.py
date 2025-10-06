from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.listy_chat, name='listy_chat'),
    path('widget/', views.listy_widget, name='listy_widget'),
]