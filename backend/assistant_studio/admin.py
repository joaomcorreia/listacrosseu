from django.contrib import admin
from .models import AssistantConfig, KnowledgeDoc

@admin.register(AssistantConfig)
class AssistantConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "default_lang", "updated_at")
    list_filter = ("status", "default_lang")
    search_fields = ("system_prompt",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Status & Languages", {"fields": ("status", "default_lang", "supported_langs")}),
        ("Prompt", {"fields": ("system_prompt",)}),
        ("Guardrails", {"fields": ("guardrails",)}),
        ("CTA Text", {"fields": ("cta_text",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

@admin.register(KnowledgeDoc)
class KnowledgeDocAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "type", "lang", "enabled", "priority", "embedded_at")
    list_filter = ("type", "lang", "enabled")
    search_fields = ("slug", "title")
    readonly_fields = ("checksum", "embedded_at", "created_at", "updated_at")
    fieldsets = (
        ("Basic Info", {"fields": ("slug", "title", "type", "lang", "enabled", "priority")}),
        ("Content", {"fields": ("content", "source_path", "url")}),
        ("Embedding", {"fields": ("checksum", "embedded_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )