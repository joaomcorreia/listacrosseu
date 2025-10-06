from django.apps import AppConfig


class TravelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel'
    verbose_name = 'Travel Content'
    
    def ready(self):
        """Import admin when Django starts"""
        try:
            import travel.admin
        except ImportError:
            pass