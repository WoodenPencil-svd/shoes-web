from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ORDER"
    
    def ready(self):
        import ORDER.signals  # Import signals
