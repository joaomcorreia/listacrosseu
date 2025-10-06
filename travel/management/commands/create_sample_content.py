from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from travel.models import Article, ArticleCategory, Tag, TravelItinerary, ItineraryDay, ItineraryStop
from businesses.models import Country, City, Business
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample travel content to demonstrate the CMS'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎨 Creating Sample Travel Content...'))
        
        # Get or create a superuser
        try:
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                self.stdout.write(self.style.WARNING('No superuser found. Creating sample user...'))
                author = User.objects.create_user(
                    username='travel_editor',
                    email='editor@listacrosseu.com',
                    password='demo123',
                    is_staff=True,
                    is_superuser=True
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
            return
        
        # Get some existing data
        try:
            hamburg = City.objects.filter(name__icontains='Hamburg').first()
            berlin = City.objects.filter(name__icontains='Berlin').first()
            paris = City.objects.filter(name__icontains='Paris').first()
        except:
            self.stdout.write(self.style.WARNING('Cities not found, using first available city'))
            hamburg = City.objects.first()
            berlin = City.objects.all()[1] if City.objects.count() > 1 else hamburg
            paris = City.objects.all()[2] if City.objects.count() > 2 else hamburg
        
        if not hamburg:
            self.stdout.write(self.style.ERROR('No cities found in database. Please add cities first.'))
            return
        
        # Get categories and tags
        city_guide_category = ArticleCategory.objects.filter(name='City Guides').first()
        food_category = ArticleCategory.objects.filter(name='Food & Dining').first()
        
        must_see_tag = Tag.objects.filter(name='Must See').first()
        weekend_tag = Tag.objects.filter(name='Weekend Trip').first()
        budget_tag = Tag.objects.filter(name='Budget Travel').first()
        
        # Sample Articles
        articles_data = [
            {
                'title': f'Ultimate Guide to {hamburg.name}: A Weekend Adventure',
                'subtitle': 'Discover the maritime charm and modern culture of Germany\'s gateway city',
                'excerpt': f'From historic warehouses to trendy neighborhoods, {hamburg.name} offers the perfect blend of tradition and innovation. This comprehensive guide covers everything you need for an unforgettable weekend.',
                'content': f'''# Welcome to {hamburg.name}!

{hamburg.name} is a city that perfectly balances its rich maritime heritage with cutting-edge culture and cuisine. Whether you're here for a weekend getaway or a longer stay, this guide will help you discover the best the city has to offer.

## Getting Around

The city's excellent public transport system makes it easy to explore all neighborhoods. Consider getting a Hamburg Card for unlimited transport and discounts at attractions.

## Must-See Attractions

### Historic Speicherstadt
The world's largest warehouse district is now a UNESCO World Heritage site. Walk through the red-brick buildings and visit the Miniatur Wunderland.

### HafenCity
Europe's largest urban development project offers modern architecture, waterfront dining, and the stunning Elbphilharmonie concert hall.

### St. Pauli and Reeperbahn
The famous entertainment district comes alive at night with theaters, clubs, and restaurants.

## Food & Dining

Don't miss the traditional Fischmarkt on Sunday mornings, where you can sample fresh seafood and local specialties.

## Shopping

From the elegant shopping arcades in the city center to the trendy boutiques in Schanzenviertel, {hamburg.name} offers shopping for every taste and budget.

## Practical Tips

- Most restaurants close between 3-6 PM
- Tipping 10% is standard
- English is widely spoken in tourist areas
- Book restaurant reservations in advance''',
                'article_type': 'guide',
                'category': city_guide_category,
                'city': hamburg,
                'tags': [must_see_tag, weekend_tag] if must_see_tag and weekend_tag else [],
                'status': 'published',
                'featured': True
            },
            {
                'title': f'Best Budget Eats in {berlin.name}' if berlin != hamburg else 'Hidden Gems: Local Favorites',
                'subtitle': 'Delicious meals under €15 that locals actually love',
                'excerpt': 'Discover amazing local restaurants where you can eat well without breaking the bank. From traditional cuisine to modern fusion, these spots offer incredible value.',
                'content': '''# Eating Well on a Budget

Finding great food that doesn't cost a fortune is one of travel's greatest pleasures. Here are our top picks for budget-friendly dining that doesn't compromise on quality or authenticity.

## Traditional Cuisine

### Local Markets
Visit the morning markets for fresh, affordable breakfast and snacks. Many vendors offer samples!

### Family-Run Restaurants
Look for places where locals eat lunch. These often offer the best value and most authentic experience.

## International Options

The city's diverse population means excellent international cuisine at great prices.

### Asian District
Fresh noodle soups, dumplings, and curries that rival expensive restaurants.

### Mediterranean Quarter
Authentic pizzas, kebabs, and tapas at student-friendly prices.

## Insider Tips

- Lunch specials (usually 11 AM - 3 PM) offer the best value
- Happy hour isn't just for drinks - many places offer food discounts too
- Street food festivals happen regularly and showcase the best local vendors
- University areas always have great cheap eats

## Money-Saving Strategies

1. Eat your main meal at lunch when portions are larger and prices lower
2. Share plates - many restaurants serve generous portions
3. Look for "daily specials" written on chalkboards
4. Ask locals for recommendations - they know the hidden gems''',
                'article_type': 'tips',
                'category': food_category,
                'city': berlin if berlin != hamburg else hamburg,
                'tags': [budget_tag] if budget_tag else [],
                'status': 'published',
                'featured': False
            }
        ]
        
        created_articles = 0
        for article_data in articles_data:
            tags = article_data.pop('tags', [])
            city = article_data.pop('city')
            
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    **article_data,
                    'author': author,
                    'published_at': timezone.now() if article_data['status'] == 'published' else None
                }
            )
            
            if created:
                # Add city and tags
                if city:
                    article.cities.add(city)
                    if city.country:
                        article.countries.add(city.country)
                
                for tag in tags:
                    if tag:
                        article.tags.add(tag)
                
                created_articles += 1
                self.stdout.write(f"  ✅ Created article: {article.title}")
        
        # Sample Itinerary
        if hamburg:
            itinerary_data = {
                'title': f'Perfect Day in {hamburg.name}',
                'description': f'A carefully planned day exploring the highlights of {hamburg.name}, from morning coffee to evening entertainment.',
                'city': hamburg,
                'duration_type': 'full_day',
                'total_cost_estimate': 75.00,
                'is_published': True,
                'author': author,
                'featured': True
            }
            
            itinerary, created = TravelItinerary.objects.get_or_create(
                title=itinerary_data['title'],
                defaults=itinerary_data
            )
            
            if created:
                self.stdout.write(f"  📅 Created itinerary: {itinerary.title}")
                
                # Create a sample day
                day = ItineraryDay.objects.create(
                    itinerary=itinerary,
                    day_number=1,
                    title='Exploring the City',
                    description='A full day of sightseeing, culture, and cuisine'
                )
                
                # Sample stops
                stops = [
                    {
                        'title': 'Morning Coffee & Pastries',
                        'description': 'Start your day at a traditional café',
                        'time_slot': 'morning',
                        'duration_minutes': 60,
                        'estimated_cost': 8.50,
                        'tips': 'Try the local breakfast specialties'
                    },
                    {
                        'title': 'Historic District Walking Tour',
                        'description': 'Explore the old town and waterfront',
                        'time_slot': 'morning',
                        'duration_minutes': 150,
                        'estimated_cost': 0.00,
                        'tips': 'Wear comfortable walking shoes'
                    },
                    {
                        'title': 'Lunch at Local Restaurant',
                        'description': 'Traditional cuisine at a family-run establishment',
                        'time_slot': 'afternoon',
                        'duration_minutes': 90,
                        'estimated_cost': 18.00,
                        'tips': 'Ask for the daily special'
                    },
                    {
                        'title': 'Museum or Gallery Visit',
                        'description': 'Cultural immersion and local art',
                        'time_slot': 'afternoon',
                        'duration_minutes': 120,
                        'estimated_cost': 12.00,
                        'tips': 'Check for student or senior discounts'
                    },
                    {
                        'title': 'Dinner & Evening Entertainment',
                        'description': 'End the day with great food and local nightlife',
                        'time_slot': 'evening',
                        'duration_minutes': 180,
                        'estimated_cost': 35.00,
                        'tips': 'Make reservations in advance'
                    }
                ]
                
                for i, stop_data in enumerate(stops):
                    ItineraryStop.objects.create(
                        day=day,
                        sort_order=i,
                        **stop_data
                    )
                
                self.stdout.write(f"    📍 Added {len(stops)} stops to itinerary")
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n🎉 Sample Content Created!'))
        self.stdout.write(f"📊 Articles: {Article.objects.count()}")
        self.stdout.write(f"📊 Itineraries: {TravelItinerary.objects.count()}")
        self.stdout.write(f"📊 Categories: {ArticleCategory.objects.count()}")
        self.stdout.write(f"📊 Tags: {Tag.objects.count()}")
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("✨ YOUR TRAVEL CMS IS READY!"))
        self.stdout.write("🌐 Visit: http://127.0.0.1:8000/admin/travel/")
        self.stdout.write("📝 Start editing articles and creating more content")
        self.stdout.write("🗺️ Build detailed itineraries for your favorite cities")
        self.stdout.write("📊 Track analytics and optimize your content strategy")