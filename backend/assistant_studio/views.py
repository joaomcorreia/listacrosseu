import os
import json
from django.db import transaction
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AssistantConfig, AssistantVersion, KnowledgeDoc, Intent
from .serializers import AssistantLiveSerializer, AssistantUpdateSerializer, AssistantVersionSerializer, KnowledgeDocSerializer, KnowledgeDocListSerializer, IntentSerializer, IntentListSerializer, get_live_config
from .runtime import detect_lang, score_intent, select_kb, render_template_answer, choose_cta_text, tool_payload_template

def get_editable_config():
    # Prefer the most recently updated row (draft or live); you can refine to explicit "draft" later.
    obj = AssistantConfig.objects.order_by("-updated_at").first()
    return obj

def snapshot_payload(cfg: AssistantConfig) -> dict:
    kb = list(
        KnowledgeDoc.objects.filter(enabled=True).values(
            "slug","title","type","lang","priority","embedded_at"
        )
    )
    intents = list(
        Intent.objects.filter(enabled=True).order_by("-priority","name").values(
            "name","title","answer_style","primary_cta","fallback_doc_slugs","examples","keywords"
        )
    )
    return {
        "status": cfg.status,
        "default_lang": cfg.default_lang,
        "supported_langs": cfg.supported_langs,
        "system_prompt": cfg.system_prompt,
        "guardrails": cfg.guardrails,
        "cta_text": cfg.cta_text,
        "kb": kb,
        "intents": intents,
        "updated_at": cfg.updated_at.isoformat(),
    }

class AssistantLiveView(APIView):
    authentication_classes = []  # adjust later if you want auth
    permission_classes = []      # public read is fine for now

    def get(self, request):
        obj = get_live_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=status.HTTP_404_NOT_FOUND)
        data = AssistantLiveSerializer(obj).data
        return Response(data, status=status.HTTP_200_OK)

class AssistantConfigView(APIView):
    authentication_classes = []   # TODO: tighten when auth is ready (Session/JWT)
    permission_classes = []       # TODO: restrict to staff/admin dashboard

    def get(self, request):
        obj = get_editable_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=status.HTTP_404_NOT_FOUND)
        data = AssistantLiveSerializer(obj).data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        obj = get_editable_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssistantUpdateSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AssistantLiveSerializer(obj).data, status=status.HTTP_200_OK)


class AssistantPublishView(APIView):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        obj = get_editable_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=404)

        label = request.data.get("label", "")
        make_live = bool(request.data.get("make_live", True))

        # compute next version
        last = obj.versions.order_by("-version").first()
        next_ver = 1 if not last else last.version + 1

        snap = snapshot_payload(obj)
        av = AssistantVersion.objects.create(config=obj, version=next_ver, label=label, payload=snap)

        if make_live:
            obj.status = "live"
            obj.save(update_fields=["status", "updated_at"])

        return Response({
            "published": True,
            "version": next_ver,
            "live": obj.status == "live",
            "item": AssistantVersionSerializer(av).data
        }, status=201)


class AssistantVersionsListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        obj = get_editable_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=404)
        data = AssistantVersionSerializer(obj.versions.all(), many=True).data
        return Response({"versions": data}, status=200)


class AssistantRollbackView(APIView):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request, version: int):
        obj = get_editable_config()
        if not obj:
            return Response({"detail": "No assistant config found."}, status=404)
        try:
            ver = obj.versions.get(version=version)
        except AssistantVersion.DoesNotExist:
            return Response({"detail": "Version not found."}, status=404)

        payload = ver.payload or {}
        # restore fields (keep status as draft unless explicitly make_live)
        obj.system_prompt = payload.get("system_prompt", obj.system_prompt)
        obj.default_lang = payload.get("default_lang", obj.default_lang)
        obj.supported_langs = payload.get("supported_langs", obj.supported_langs)
        obj.guardrails = payload.get("guardrails", obj.guardrails)
        obj.cta_text = payload.get("cta_text", obj.cta_text)
        obj.save()

        make_live = bool(request.data.get("make_live", False))
        if make_live:
            obj.status = "live"
            obj.save(update_fields=["status", "updated_at"])

        return Response(AssistantLiveSerializer(obj).data, status=200)


class KnowledgeDocsView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        qs = KnowledgeDoc.objects.all().order_by("-enabled","-priority","slug")
        return Response({"items": KnowledgeDocListSerializer(qs, many=True).data}, status=200)

    def post(self, request):
        # create
        ser = KnowledgeDocSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(KnowledgeDocSerializer(obj).data, status=201)

    def patch(self, request):
        # update by id or slug
        pk = request.data.get("id")
        slug = request.data.get("slug")
        obj = None
        if pk:
            obj = KnowledgeDoc.objects.filter(id=pk).first()
        elif slug:
            obj = KnowledgeDoc.objects.filter(slug=slug).first()
        if not obj:
            return Response({"detail":"KB doc not found."}, status=404)
        ser = KnowledgeDocSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(KnowledgeDocSerializer(obj).data, status=200)


class KnowledgeEmbedView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Stub: mark embedded_at + checksum; real embedding comes later
        pk = request.data.get("id")
        slug = request.data.get("slug")
        obj = None
        if pk:
            obj = KnowledgeDoc.objects.filter(id=pk).first()
        elif slug:
            obj = KnowledgeDoc.objects.filter(slug=slug).first()
        if not obj:
            return Response({"detail":"KB doc not found."}, status=404)

        # compute simple checksum from content/path/url for now
        import hashlib
        material = (obj.content or obj.source_path or obj.url or "").encode("utf-8", errors="ignore")
        obj.checksum = hashlib.sha256(material).hexdigest()
        obj.embedded_at = timezone.now()
        obj.save(update_fields=["checksum","embedded_at","updated_at"])
        return Response({"status":"ok","id":obj.id,"embedded_at":obj.embedded_at}, status=200)


# Action endpoint views
import hashlib
import re
import time
from django.utils.text import slugify
from .serializers import (
    CreateListingRequest, StartJCWBuildRequest, StartPrintOrderRequest
)

SAFE_SLUG_RE = re.compile(r"[^a-z0-9\-]+")

def short_hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:8]

class CreateListingActionView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        ser = CreateListingRequest(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        # Stub: generate a fake listing + dashboard URL
        name_slug = slugify(data["business_name"]) or "business"
        city_slug = slugify(data["city"]) or "city"
        country = data["country"].lower()
        code = short_hash(f'{data["business_name"]}|{country}|{city_slug}|{time.time()}')

        listing_url = f"/{country}/{city_slug}/business/{name_slug}-{code}"
        dashboard_url = f"/dashboard/listings/{code}"

        return Response({
            "status": "ok",
            "listing_url": listing_url,
            "dashboard_url": dashboard_url
        }, status=status.HTTP_200_OK)

class StartJCWBuildActionView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        ser = StartJCWBuildRequest(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        # Stub: issue a pretend builder session URL
        sess = short_hash(f'{data["tenant_id"]}|{time.time()}')
        redirect_url = f"https://builder.justcodeworks.eu/session/{sess}"

        return Response({"status": "ok", "redirect_url": redirect_url}, status=200)

class StartPrintOrderActionView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        ser = StartPrintOrderRequest(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        # Stub: pretend we created a draft order
        oid = short_hash(f'{data["product"]}|{data["quantity"]}|{time.time()}')
        redirect_url = f"/print/order/{oid}"

        return Response({"status": "ok", "redirect_url": redirect_url}, status=200)


class IntentsView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        qs = Intent.objects.all().order_by("-enabled","-priority","name")
        return Response({"items": IntentListSerializer(qs, many=True).data}, status=200)

    def post(self, request):
        ser = IntentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(IntentSerializer(obj).data, status=201)

    def patch(self, request):
        pk = request.data.get("id")
        name = request.data.get("name")
        obj = Intent.objects.filter(id=pk).first() if pk else Intent.objects.filter(name=name).first()
        if not obj:
            return Response({"detail":"Intent not found."}, status=404)
        ser = IntentSerializer(obj, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(IntentSerializer(obj).data, status=200)


class AssistantAskView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        q = (request.data.get("q") or "").strip()
        lang_req = (request.data.get("lang") or "").strip().lower()
        if not q:
            return Response({"detail":"q is required"}, status=400)

        cfg = get_live_config()
        if not cfg:
            return Response({"detail":"assistant not configured"}, status=503)

        lang = detect_lang(lang_req, cfg)
        intents = list(Intent.objects.all())
        routed = score_intent(intents, q)
        it = routed["intent"]

        kb_docs = select_kb(lang, limit=4)

        # Try LLM if configured
        provider = (os.getenv("LLM_PROVIDER") or "").lower()
        llm_text = None
        try:
            if provider == "openai" and os.getenv("OPENAI_API_KEY"):
                from .runtime import llm_answer_openai
                llm_text = llm_answer_openai(cfg.system_prompt, lang, q, it, kb_docs)
        except Exception:
            llm_text = None

        answer = llm_text or render_template_answer(cfg, it, lang, kb_docs, q)
        cta_code = (it.primary_cta if it else "none")
        cta_label = choose_cta_text(cfg, cta_code, lang)
        payload_tmpl = tool_payload_template(it, lang)

        return Response({
            "lang": lang,
            "intent": (it.name if it else None),
            "answer": answer,
            "cta": {
                "code": cta_code,
                "label": cta_label
            },
            "tool_payload_template": payload_tmpl,
            "used_kb": [ {"slug": d.slug, "title": d.title, "lang": d.lang, "type": d.type} for d in kb_docs ]
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AssistantSimpleAskView(APIView):
    """
    Simple assistant endpoint for Step 11 - handles POST requests and calls OpenAI
    Endpoint: /assistant/api/ask/
    Expected JSON: {"message": "hello there"}
    Returns JSON: {"reply": "<assistant message>", "status": "ok"}
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        import json
        
        # Log incoming request
        print(f"[AssistantAPI] Incoming request: {request.data}")
        
        try:
            # Get message from request body
            message = request.data.get("message", "").strip()
            
            if not message:
                print("[AssistantAPI] Empty message received")
                return Response({
                    "reply": "Empty message", 
                    "status": "error"
                }, status=400)
            
            # Check if OpenAI API key is available
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                print("[AssistantAPI] No OpenAI API key found")
                return Response({
                    "reply": "Sorry, I'm having trouble answering right now.",
                    "status": "error"
                }, status=500)
            
            # Try to call OpenAI
            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_api_key)
                
                print(f"[AssistantAPI] Calling OpenAI with message: {message}")
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant for ListAcrossEU, a European business directory. Keep responses concise and helpful."
                        },
                        {
                            "role": "user", 
                            "content": message
                        }
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                
                reply = response.choices[0].message.content.strip()
                
                print(f"[AssistantAPI] OpenAI response: {reply}")
                
                return Response({
                    "reply": reply,
                    "status": "ok"
                }, status=200)
                
            except Exception as openai_error:
                print(f"[AssistantAPI] OpenAI error: {openai_error}")
                return Response({
                    "reply": "Sorry, I'm having trouble answering right now.",
                    "status": "error"
                }, status=500)
                
        except Exception as e:
            print(f"[AssistantAPI] General error: {e}")
            return Response({
                "reply": "Sorry, I'm having trouble answering right now.",
                "status": "error"
            }, status=500)

