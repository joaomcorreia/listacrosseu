from rest_framework.generics import RetrieveAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from .models import Page
from .serializers import PageSerializer


class PageDetail(RetrieveAPIView):
    serializer_class = PageSerializer
    lookup_field = "slug"
    
    def get_object(self):
        slug = self.kwargs["slug"]
        lang = self.kwargs.get("lang", "en")
        return get_object_or_404(Page, slug=slug, language=lang, is_published=True)


class PageList(ListAPIView):
    serializer_class = PageSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get("lang", "en")
        return Page.objects.filter(language=lang, is_published=True).order_by("slug")
