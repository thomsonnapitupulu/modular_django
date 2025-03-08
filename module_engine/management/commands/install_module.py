# module_engine/management/commands/install_module.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import importlib
import os

from module_engine.models import Module


class Command(BaseCommand):
    help = 'Install a module by identifier'
    
    def add_arguments(self, parser):
        parser.add_argument('module_id', type=str, help='Module identifier')
    
    def handle(self, *args, **options):
        module_id = options['module_id']
        
        try:
            # Check if module exists in database
            try:
                module = Module.objects.get(identifier=module_id)
            except Module.DoesNotExist:
                raise CommandError(f"Module '{module_id}' not found in registry.")
            
            # Check if the module package exists
            try:
                importlib.import_module(module_id)
            except ImportError:
                raise CommandError(f"Module package '{module_id}' not found in Python path.")
            
            # Get the module info
            try:
                module_info = importlib.import_module(f"{module_id}.module_info")
                if not hasattr(module_info, 'MODULE_INFO'):
                    raise CommandError(f"Module '{module_id}' does not have MODULE_INFO defined.")
            except ImportError:
                raise CommandError(f"Module '{module_id}' does not have a module_info.py file.")
            
            # Update settings to include the module
            settings_path = os.path.join(settings.BASE_DIR, 'modular_django', 'settings.py')
            with open(settings_path, 'r') as f:
                content = f.read()
            
            if f"'{module_id}'" not in content and f'"{module_id}"' not in content:
                # Add to INSTALLED_APPS
                new_content = content.replace(
                    'INSTALLED_APPS = [',
                    f'INSTALLED_APPS = [\n    "{module_id}",'
                )
                
                with open(settings_path, 'w') as f:
                    f.write(new_content)
                
                self.stdout.write(self.style.SUCCESS(f"Added '{module_id}' to INSTALLED_APPS"))
            else:
                self.stdout.write(f"Module '{module_id}' already in INSTALLED_APPS")
            
            # Update module status in database
            module.installed = True
            module.active = True
            module.version = module_info.MODULE_INFO['version']
            module.save()
            
            self.stdout.write(self.style.SUCCESS(f"Module '{module_id}' installed successfully"))
            
            # Reminder about migrations
            self.stdout.write(
                "Don't forget to run migrations:\n"
                f"  python manage.py makemigrations {module_id}\n"
                f"  python manage.py migrate {module_id}"
            )
            
        except Exception as e:
            raise CommandError(f"Failed to install module: {str(e)}")