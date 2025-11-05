from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class Command(BaseCommand):
    help = 'Test and fix admin login'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking Admin Login...'))
        self.stdout.write(f"User model: {User}")
        self.stdout.write(f"Username field: {User.USERNAME_FIELD}")
        self.stdout.write(f"Required fields: {User.REQUIRED_FIELDS}")
        
        admin_email = 'admin@listacrosseu.com'
        admin_password = 'admin123'
        
        try:
            # Check if admin user exists (by email since that's the USERNAME_FIELD)
            admin = User.objects.get(email=admin_email)
            self.stdout.write(f"✅ Admin user found: {admin.email}")
            self.stdout.write(f"   Username: {admin.username}")
            self.stdout.write(f"   Email: {admin.email}")
            self.stdout.write(f"   Is Active: {admin.is_active}")
            self.stdout.write(f"   Is Staff: {admin.is_staff}")
            self.stdout.write(f"   Is Superuser: {admin.is_superuser}")
            
            # Test password authentication (use email as username)
            user = authenticate(username=admin_email, password=admin_password)
            if user:
                self.stdout.write(f"✅ Password authentication works!")
            else:
                self.stdout.write(f"❌ Password authentication failed!")
                # Reset password
                admin.set_password(admin_password)
                admin.is_active = True
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                self.stdout.write(f"🔧 Password and permissions reset")
                
                # Test again
                user = authenticate(username=admin_email, password=admin_password)
                if user:
                    self.stdout.write(f"✅ Password now works!")
                else:
                    self.stdout.write(f"❌ Still not working - creating new admin")
                    # Delete and recreate
                    admin.delete()
                    new_admin = User.objects.create_user(
                        email=admin_email,
                        username='admin',
                        password=admin_password,
                        first_name='Admin',
                        last_name='User',
                        is_staff=True,
                        is_superuser=True,
                        is_active=True
                    )
                    self.stdout.write(f"✅ Created fresh admin user")
            
        except User.DoesNotExist:
            self.stdout.write(f"❌ Admin user not found - creating new one")
            admin = User.objects.create_user(
                email=admin_email,
                username='admin',
                password=admin_password,
                first_name='Admin',
                last_name='User',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write(f"✅ Created admin user")
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Login Ready!'))
        self.stdout.write("=" * 50)
        self.stdout.write(f"🌐 URL: http://127.0.0.1:8000/admin/login/")
        self.stdout.write(f"👤 Email (Username): {admin_email}")
        self.stdout.write(f"🔑 Password: {admin_password}")
        self.stdout.write("=" * 50)
        self.stdout.write("\n💡 IMPORTANT: Use EMAIL as username, not 'admin'!")