from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin user for travel CMS access'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔑 Creating Admin User...'))
        
        # Create or update admin user
        username = 'admin'
        email = 'admin@listacrosseu.com'
        password = 'admin123'
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        
        # Set password (works for both new and existing users)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(f"✅ Created new admin user: {username}")
        else:
            self.stdout.write(f"✅ Updated existing admin user: {username}")
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Admin Access Ready!'))
        self.stdout.write("=" * 50)
        self.stdout.write(f"🌐 URL: http://127.0.0.1:8000/admin/")
        self.stdout.write(f"👤 Username: {username}")
        self.stdout.write(f"🔑 Password: {password}")
        self.stdout.write("=" * 50)
        self.stdout.write("\n💡 After logging in, go to:")
        self.stdout.write("   📝 /admin/travel/ - Travel Content Management")
        self.stdout.write("   🏢 /admin/businesses/ - Business Directory")
        self.stdout.write("   🔍 /admin/duplicate-detection/ - Duplicate Management")
        
        # Also create the travel author user with proper password
        travel_user, created = User.objects.get_or_create(
            username='travel_author',
            defaults={
                'email': 'travel@listacrosseu.com',
                'first_name': 'Travel',
                'last_name': 'Author',
                'is_staff': True,  # Make staff so they can access admin
            }
        )
        travel_user.set_password('travel123')
        travel_user.is_staff = True
        travel_user.save()
        
        if created:
            self.stdout.write(f"✅ Created travel author user: travel_author")
        else:
            self.stdout.write(f"✅ Updated travel author user: travel_author")