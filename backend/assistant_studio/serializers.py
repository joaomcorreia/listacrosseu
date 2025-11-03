from rest_framework import serializers
from .models import AssistantConfig, AssistantVersion, KnowledgeDoc, Intent

class AssistantLiveSerializer(serializers.ModelSerializer):
    version = serializers.SerializerMethodField()

    class Meta:
        model = AssistantConfig
        fields = (
            "version",
            "status",
            "default_lang",
            "supported_langs",
            "system_prompt",
            "guardrails",
            "cta_text",
            "updated_at",
        )

    def get_version(self, obj):
        # Simple monotonic version based on pk + updated_at timestamp
        return f"{obj.pk}-{int(obj.updated_at.timestamp())}"

class AssistantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantConfig
        fields = (
            "status",          # draft | live | archived (keep as draft while editing)
            "default_lang",
            "supported_langs",
            "system_prompt",
            "guardrails",
            "cta_text",
        )


class AssistantVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantVersion
        fields = ("version", "label", "payload", "created_at")


class KnowledgeDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDoc
        fields = (
            "id","slug","title","type","lang","enabled","priority",
            "content","source_path","url","checksum","embedded_at",
            "created_at","updated_at"
        )


class KnowledgeDocListSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDoc
        fields = ("id","slug","title","type","lang","enabled","priority","embedded_at","updated_at")


class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = (
            "id","name","title","enabled","priority",
            "examples","keywords","answer_style","primary_cta","fallback_doc_slugs",
            "created_at","updated_at"
        )

class IntentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = ("id","name","title","enabled","priority","answer_style","primary_cta","updated_at")

def get_live_config():
    qs_live = AssistantConfig.objects.filter(status="live").order_by("-updated_at")
    obj = qs_live.first()
    if obj:
        return obj
    # Fallback to most recent draft if no live exists yet
    return AssistantConfig.objects.order_by("-updated_at").first()


# Action endpoint serializers
class CreateListingRequest(serializers.Serializer):
    business_name = serializers.CharField(max_length=160)
    country = serializers.CharField(max_length=2)
    city = serializers.CharField(max_length=120)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=64)

class StartJCWBuildRequest(serializers.Serializer):
    tenant_id = serializers.CharField(max_length=120)
    preferred_locales = serializers.ListField(child=serializers.CharField(max_length=5), allow_empty=True)
    template_id = serializers.CharField(max_length=80)

class StartPrintOrderRequest(serializers.Serializer):
    product = serializers.CharField(max_length=80)
    quantity = serializers.IntegerField(min_value=1)