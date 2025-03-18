"""Dynamic settings loader for modular Django"""
import importlib
import sys

def get_installed_modules():
    """
    Get installed modules from the database.
    Called from settings.py to dynamically add installed modules to INSTALLED_APPS.
    """
    try:
        # We need to import Module model, but we can't import it directly
        # as it might create a circular import.
        # We'll use a workaround with importlib
        module_engine = importlib.import_module('module_engine.models')
        Module = getattr(module_engine, 'Module')
        
        # Get all installed and active modules
        installed_modules = list(Module.objects.filter(installed=True, active=True).values_list('identifier', flat=True))
        return installed_modules
    except Exception as e:
        # During initial setup/migrations, the Module model might not exist yet
        # In that case, return an empty list
        return []