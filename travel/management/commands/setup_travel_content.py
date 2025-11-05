from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from travel.models import ArticleCategory, Tag
from businesses.models import Country, City

User = get_user_model()


class Command(BaseCommand):
    help = 'Create initial travel content categories and tags'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌍 Creating Travel Content Setup...'))
        
        # Create Article Categories
        categories = [
            {
                'name': 'City Guides',
                'description': 'Comprehensive guides to European cities',
                'icon': '🏙️',
                'color': '#007cba'
            },
            {
                'name': 'Food & Dining',
                'description': 'Restaurant reviews, food tours, and culinary experiences',
                'icon': '🍽️',
                'color': '#dc3545'
            },
            {
                'name': 'Shopping',
                'description': 'Shopping districts, markets, and retail experiences',
                'icon': '🛍️',
                'color': '#28a745'
            },
            {
                'name': 'Culture & History',
                'description': 'Museums, historical sites, and cultural experiences',
                'icon': '🏛️',
                'color': '#6f42c1'
            },
            {
                'name': 'Nightlife & Entertainment',
                'description': 'Bars, clubs, theaters, and entertainment venues',
                'icon': '🌃',
                'color': '#fd7e14'
            },
            {
                'name': 'Transportation',
                'description': 'Getting around European cities',
                'icon': '🚇',
                'color': '#20c997'
            },
            {
                'name': 'Accommodation',
                'description': 'Hotels, hostels, and places to stay',
                'icon': '🏨',
                'color': '#17a2b8'
            },
            {
                'name': 'Seasonal Events',
                'description': 'Festivals, markets, and seasonal activities',
                'icon': '🎭',
                'color': '#e83e8c'
            },
            {
                'name': 'Business Spotlights',
                'description': 'Featured businesses and local entrepreneurs',
                'icon': '⭐',
                'color': '#ffc107'
            },
            {
                'name': 'Travel Tips',
                'description': 'Practical advice for European travel',
                'icon': '💡',
                'color': '#6c757d'
            }
        ]
        
        created_categories = 0
        for cat_data in categories:
            category, created = ArticleCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                created_categories += 1
                self.stdout.write(f"  ✅ Created category: {category.name}")
        
        self.stdout.write(f"📂 Created {created_categories} article categories")
        
        # Create Tags
        tags = [
            {'name': 'Budget Travel', 'color': '#28a745'},
            {'name': 'Luxury', 'color': '#6f42c1'},
            {'name': 'Family Friendly', 'color': '#17a2b8'},
            {'name': 'Solo Travel', 'color': '#fd7e14'},
            {'name': 'Couples', 'color': '#e83e8c'},
            {'name': 'Business Travel', 'color': '#6c757d'},
            {'name': 'Weekend Trip', 'color': '#20c997'},
            {'name': 'Hidden Gems', 'color': '#dc3545'},
            {'name': 'Must See', 'color': '#ffc107'},
            {'name': 'Local Experience', 'color': '#007cba'},
            {'name': 'Historic', 'color': '#6f42c1'},
            {'name': 'Modern', 'color': '#17a2b8'},
            {'name': 'Outdoor', 'color': '#28a745'},
            {'name': 'Indoor', 'color': '#fd7e14'},
            {'name': 'Accessible', 'color': '#20c997'},
            {'name': 'Trendy', 'color': '#e83e8c'},
            {'name': 'Traditional', 'color': '#dc3545'},
            {'name': 'Seasonal', 'color': '#ffc107'},
        ]
        
        created_tags = 0
        for tag_data in tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            if created:
                created_tags += 1
                self.stdout.write(f"  🏷️ Created tag: {tag.name}")
        
        self.stdout.write(f"🏷️ Created {created_tags} tags")
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n🎉 Travel Content Setup Complete!'))
        self.stdout.write(f"📊 Total Categories: {ArticleCategory.objects.count()}")
        self.stdout.write(f"📊 Total Tags: {Tag.objects.count()}")
        self.stdout.write("\n💡 You can now start creating travel articles in the admin!")
        self.stdout.write("   📝 Go to: /admin/travel/")
        
        # Show some quick start tips
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("🚀 QUICK START TIPS:"))
        self.stdout.write("1. 📝 Create your first city guide article")
        self.stdout.write("2. 🏪 Link businesses to articles for featured content")
        self.stdout.write("3. 🗺️ Build travel itineraries with day-by-day planning")
        self.stdout.write("4. 🏷️ Use tags to organize content by travel style")
        self.stdout.write("5. 📈 Monitor analytics to see what content performs best")