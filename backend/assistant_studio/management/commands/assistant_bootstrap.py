from django.core.management.base import BaseCommand
from assistant_studio.models import AssistantConfig

DEFAULT_PROMPT = (
    "You are the ListAcross EU Assistant. Help users understand Free vs Paid, "
    "explain upgrades, and bridge to Just Code Works for full websites and printing. "
    "Keep answers concise and multilingual (EN/NL/FR/ES/PT). Prefer retrieved knowledge; "
    "if unknown, say so briefly and offer a clear next step. Show at most one primary CTA."
)

DEFAULT_CTA = {
    "en": {
        "create_listing": "Advertise free",
        "upgrade_plan": "Upgrade plan",
        "start_jcw_build": "Build my website",
        "start_print_order": "Order business cards"
    },
    "nl": {
        "create_listing": "Adverteren gratis",
        "upgrade_plan": "Upgraden",
        "start_jcw_build": "Website bouwen",
        "start_print_order": "Visitekaartjes bestellen"
    },
    "pt": {
        "create_listing": "Anunciar grátis",
        "upgrade_plan": "Atualizar plano",
        "start_jcw_build": "Construir meu website",
        "start_print_order": "Encomendar cartões"
    }
}

class Command(BaseCommand):
    help = "Create a default AssistantConfig if none exists."

    def handle(self, *args, **options):
        obj = AssistantConfig.objects.first()
        if obj:
            self.stdout.write(self.style.WARNING(f"AssistantConfig already exists: id={obj.id}"))
            return
        obj = AssistantConfig.objects.create(
            status="draft",
            default_lang="en",
            supported_langs=["en", "nl", "fr", "es", "pt"],
            system_prompt=DEFAULT_PROMPT,
            guardrails={"pricing_requires_doc": True},
            cta_text=DEFAULT_CTA,
        )
        self.stdout.write(self.style.SUCCESS(f"Created AssistantConfig id={obj.id}"))