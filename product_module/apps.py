# product_module/apps.py
from django.apps import AppConfig


class ProductModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_module'
    verbose_name = "Product Management"
    
    def ready(self):
        # Just import the signals - no need to connect them here
        import product_module.permissions