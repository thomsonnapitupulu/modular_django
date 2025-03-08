# module_engine/management/commands/upgrade_module.py
from django.core.management.base import BaseCommand, CommandError
import importlib

from module_engine.models import Module


class Command(BaseCommand):
    help = 'Upgrade a module by identifier'
    
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
            
            if not module.installed:
                raise CommandError(f"Module '{module_id}' is not installed. Install it first.")
            
            # Get the module info
            try:
                module_info = importlib.import_module(f"{module_id}.module_info")
                if not hasattr(module_info, 'MODULE_INFO'):
                    raise CommandError(f"Module '{module_id}' does not have MODULE_INFO defined.")
            except ImportError:
                raise CommandError(f"Module '{module_id}' does not have a module_info.py file.")
            
            current_version = module.version
            new_version = module_info.MODULE_INFO['version']
            
            if current_version == new_version:
                self.stdout.write(f"Module '{module_id}' is already at version {new_version}")
                return
            
            # Update module version in database
            module.version = new_version
            module.save()
            
            self.stdout.write(self.style.SUCCESS(
                f"Module '{module_id}' upgraded from {current_version} to {new_version}"
            ))
            
            # Reminder about migrations
            self.stdout.write(
                "Don't forget to run migrations to apply any schema changes:\n"
                f"  python manage.py makemigrations {module_id}\n"
                f"  python manage.py migrate {module_id}"
            )
            
        except Exception as e:
            raise CommandError(f"Failed to upgrade module: {str(e)}")