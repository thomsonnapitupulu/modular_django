# module_engine/management/commands/uninstall_module.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

from module_engine.models import Module


class Command(BaseCommand):
    help = 'Uninstall a module by identifier'
    
    def add_arguments(self, parser):
        parser.add_argument('module_id', type=str, help='Module identifier')
        parser.add_argument('--force', action='store_true', help='Force uninstallation even if module not found')
    
    def handle(self, *args, **options):
        module_id = options['module_id']
        force = options['force']
        
        try:
            # Check if module exists in database
            try:
                module = Module.objects.get(identifier=module_id)
            except Module.DoesNotExist:
                if not force:
                    raise CommandError(f"Module '{module_id}' not found in registry.")
                self.stdout.write(f"Module '{module_id}' not found in registry. Proceeding with removal from settings.")
            
            # Update settings to remove the module
            settings_path = os.path.join(settings.BASE_DIR, 'modular_django', 'settings.py')
            with open(settings_path, 'r') as f:
                content = f.read()
            
            # Patterns to search for
            patterns = [
                f'    "{module_id}",\n',
                f"    '{module_id}',\n",
                f'    "{module_id}"\n',
                f"    '{module_id}'\n"
            ]
            
            modified = False
            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, '')
                    modified = True
            
            if modified:
                with open(settings_path, 'w') as f:
                    f.write(content)
                self.stdout.write(self.style.SUCCESS(f"Removed '{module_id}' from INSTALLED_APPS"))
            else:
                self.stdout.write(f"Module '{module_id}' not found in INSTALLED_APPS")
            
            # Update module status in database if it exists
            if 'module' in locals():
                module.installed = False
                module.active = False
                module.save()
                self.stdout.write(self.style.SUCCESS(f"Module '{module_id}' marked as uninstalled in database"))
            
            self.stdout.write(self.style.SUCCESS(f"Module '{module_id}' uninstalled successfully"))
            
        except Exception as e:
            raise CommandError(f"Failed to uninstall module: {str(e)}")