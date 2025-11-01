from django.urls import path
from .views import PageDetail, PageList

app_name = "cms"

urlpatterns = [
    path("pages/", PageList.as_view(), name="page_list"),
    path("pages/<str:lang>/<slug:slug>/", PageDetail.as_view(), name="page_detail"),
]