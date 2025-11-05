from django.contrib import messages
from .seo import suggest_for
from .images import keywords_to_sources


def apply_ai_suggestions(obj, data: dict):
    meta_json = obj.meta_json or {}
    meta_json["_ai"] = data
    
    if not obj.meta_title and data.get("title"):
        obj.meta_title = data["title"][:180]
    
    if not obj.meta_description and data.get("description"):
        obj.meta_description = data["description"][:320]
    
    imgs = data.get("images") or []
    meta_json["_ai"]["image_sources"] = keywords_to_sources([i.get("keyword", "") for i in imgs if i.get("keyword")])
    obj.meta_json = meta_json


class AIMixin:
    def ai_suggest(self, request, queryset):
        c = 0
        for obj in queryset:
            title = getattr(obj, "title", "")
            excerpt = getattr(obj, "excerpt", "") if hasattr(obj, "excerpt") else ""
            body = getattr(obj, "content", "") if hasattr(obj, "content") else getattr(obj, "body", "")
            url = getattr(obj, "canonical_url", "")
            
            data = suggest_for(title, excerpt, body, url)
            
            # AI boost by plan
            plan = getattr(getattr(obj, "visibility", None), "plan", None)
            boost = int(plan.entitlements.get("ai_boost", 0)) if plan else 0
            if boost > 0:
                data.setdefault("tags", [])
                data["tags"] = list({*data["tags"], "eu", "visibility", "listacross"})
                if isinstance(data.get("jsonld"), dict) and plan.entitlements.get("jsonld", False):
                    data["jsonld"].setdefault("about", "EU-wide business discovery")
            
            apply_ai_suggestions(obj, data)
            obj.save(update_fields=["meta_title", "meta_description", "meta_json"])
            c += 1
        
        messages.success(request, f"AI suggestions applied to {c} item(s).")
    
    ai_suggest.short_description = "AI: Suggest SEO (title/description/JSON-LD/images)"