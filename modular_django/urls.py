# modular_django/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('modules/', include('module_engine.urls')),
]

# Dynamically add module URLs from installed modules
from django.apps import apps
from importlib import import_module

# Try to import module_info from each installed app
for app_config in apps.get_app_configs():
    try:
        # Check if this app has a module_info.py file
        module_info = import_module(f"{app_config.name}.module_info")
        
        # If it has MODULE_INFO with url_prefix, add URLs
        if hasattr(module_info, 'MODULE_INFO') and 'url_prefix' in module_info.MODULE_INFO:
            prefix = module_info.MODULE_INFO['url_prefix']
            app_name = app_config.name
            
            # Add the URL pattern if the app has a urls.py
            try:
                import_module(f"{app_name}.urls")
                urlpatterns.append(
                    path(f"{prefix}/", include(f"{app_name}.urls"))
                )
            except ImportError:
                # App doesn't have a urls.py module
                pass
    except ImportError:
        # App doesn't have a module_info.py file
        pass