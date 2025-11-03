import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu.settings')
django.setup()

from assistant_studio.models import KnowledgeDoc

# Create sample KB documents
kb1 = KnowledgeDoc.objects.create(
    slug='company-faq',
    title='Company Frequently Asked Questions',
    type='faq_md',
    lang='en',
    content='# FAQ\n\n## What is our company about?\nWe help businesses across Europe.\n\n## How do we work?\nWe provide AI assistance.',
    enabled=True,
    priority=10
)

kb2 = KnowledgeDoc.objects.create(
    slug='pricing-tiers',
    title='Pricing Information',  
    type='pricing_json',
    lang='en',
    content='{"basic": {"price": 99, "features": ["Basic support", "Standard features"]}, "premium": {"price": 199, "features": ["Premium support", "All features", "Priority access"]}}',
    enabled=True,
    priority=5
)

kb3 = KnowledgeDoc.objects.create(
    slug='external-blog',
    title='External Blog Post',
    type='external_url',
    lang='en',
    url='https://example.com/blog/ai-assistance',
    enabled=False,
    priority=1
)

print(f"Created {KnowledgeDoc.objects.count()} KB documents:")
for kb in KnowledgeDoc.objects.all():
    print(f"- {kb.slug}: {kb.title} ({kb.type})")