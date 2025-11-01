from django.core.management.base import BaseCommand
from plans.models import Plan

DEFAULTS = [
    {
        "key": "free",
        "name": "Free",
        "description": "Basic presence.",
        "priority_weight": 0,
        "highlights": ["Basic meta", "Listed in category", "Upgrade-ready"],
        "entitlements": {
            "jsonld": False,
            "custom_og": False,
            "canonical_control": True,
            "ai_boost": 0,
            "max_media": 3,
            "sitemap": True,
            "allow_featured": False
        }
    },
    {
        "key": "product",
        "name": "Product Page",
        "description": "Richer profile, priority placement.",
        "priority_weight": 10,
        "highlights": ["Priority lists", "Custom OG", "More media"],
        "entitlements": {
            "jsonld": True,
            "custom_og": True,
            "canonical_control": True,
            "ai_boost": 1,
            "max_media": 12,
            "sitemap": True,
            "allow_featured": True
        }
    },
    {
        "key": "premium",
        "name": "Premium",
        "description": "EU-wide visibility, featured boosts.",
        "priority_weight": 25,
        "highlights": ["EU-wide targeting", "Full JSON-LD", "Featured & badges"],
        "entitlements": {
            "jsonld": True,
            "custom_og": True,
            "canonical_control": True,
            "ai_boost": 2,
            "max_media": 30,
            "sitemap": True,
            "allow_featured": True
        }
    },
]


class Command(BaseCommand):
    help = "Seed default plans for the platform"
    
    def handle(self, *args, **options):
        for d in DEFAULTS:
            obj, created = Plan.objects.update_or_create(key=d["key"], defaults=d)
            self.stdout.write(
                self.style.SUCCESS(f"{'Created' if created else 'Updated'} plan {obj.key}")
            )