from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from cms.models import Page
from blog.models import Post
from .seo import suggest_for
from .admin_mixins import apply_ai_suggestions


class AISuggest(APIView):
    permission_classes = [AllowAny]  # tighten later
    
    def post(self, request, *a, **kw):
        kind = request.data.get("kind")
        pk = request.data.get("id")
        title = request.data.get("title", "")
        excerpt = request.data.get("excerpt", "")
        body = request.data.get("body", "")
        url = request.data.get("url", "")
        
        data = suggest_for(title, excerpt, body, url)
        
        if kind in ("page", "post") and pk:
            obj = Page.objects.filter(pk=pk).first() if kind == "page" else Post.objects.filter(pk=pk).first()
            if obj:
                apply_ai_suggestions(obj, data)
                obj.save()
        
        return Response({"ok": True, "data": data})
