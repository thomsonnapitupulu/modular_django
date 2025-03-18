# module_engine/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import importlib
import subprocess
import sys

from .models import Module


@login_required
def module_list(request):
    """Display list of all modules and their status."""
    modules = Module.objects.all()
    
    # Discover modules
    known_modules = {m.identifier: m for m in modules}
    
    # Discover available modules
    for app in settings.INSTALLED_APPS:
        try:
            module = importlib.import_module(f"{app}.module_info")
            if hasattr(module, 'MODULE_INFO'):
                info = module.MODULE_INFO
                if info['identifier'] not in known_modules:
                    Module.objects.create(
                        name=info['name'],
                        identifier=info['identifier'],
                        version=info['version'],
                        installed=False,
                        active=False
                    )
        except (ImportError, AttributeError):
            # Not a module with MODULE_INFO
            pass
    
    # Refresh the modules list
    modules = Module.objects.all()
    
    return render(request, 'module_engine/index.html', {
        'modules': modules
    })


@login_required
def install_module(request, module_id):
    """Install a specific module."""
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':
        try:
            # Run management command to install module
            module_name = module.identifier
            
            # Check if we're in a read-only environment (like Vercel)
            readonly_env = os.environ.get('VERCEL', False)
            
            if not readonly_env:
                # For traditional deployments - update settings.py file
                settings_path = settings.BASE_DIR / 'modular_django' / 'settings.py'
                with open(settings_path, 'r') as f:
                    content = f.read()
                
                if f"'{module_name}'" not in content and f'"{module_name}"' not in content:
                    # Add to INSTALLED_APPS
                    new_content = content.replace(
                        'INSTALLED_APPS = [',
                        f'INSTALLED_APPS = [\n    "{module_name}",'
                    )
                    
                    with open(settings_path, 'w') as f:
                        f.write(new_content)
            
            # Run migrations
            subprocess.check_call([
                sys.executable, 'manage.py', 'migrate', module_name
            ])
            
            # Update module status in database (this works in both environments)
            module.installed = True
            module.active = True
            module.save()
            
            messages.success(request, _(f"Module {module.name} installed successfully."))
            
            if readonly_env:
                messages.info(request, _("You'll need to restart the application for the changes to take effect."))
                
            return redirect('module_list')
        
        except Exception as e:
            messages.error(request, _(f"Failed to install module: {str(e)}"))
    
    return render(request, 'module_engine/install.html', {
        'module': module,
        'action': 'install'
    })


@login_required
def upgrade_module(request, module_id):
    """Upgrade a specific module."""
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':
        try:
            # Get the module info
            module_name = module.identifier
            module_info = importlib.import_module(f"{module_name}.module_info")
            
            # Check if upgrade is needed
            if module.version != module_info.MODULE_INFO['version']:
                # Run migrations
                subprocess.check_call([
                    sys.executable, 'manage.py', 'makemigrations', module_name
                ])
                subprocess.check_call([
                    sys.executable, 'manage.py', 'migrate', module_name
                ])
                
                # Update module version
                module.version = module_info.MODULE_INFO['version']
                module.save()
                
                messages.success(request, _(f"Module {module.name} upgraded to version {module.version}."))
            else:
                messages.info(request, _(f"Module {module.name} is already at the latest version."))
            
            return redirect('module_list')
        
        except Exception as e:
            messages.error(request, _(f"Failed to upgrade module: {str(e)}"))
    
    return render(request, 'module_engine/install.html', {
        'module': module,
        'action': 'upgrade'
    })


@login_required
def uninstall_module(request, module_id):
    """Uninstall a specific module."""
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            try:
                # Get the module name
                module_name = module.identifier
                
                # Check if we're in a read-only environment (like Vercel)
                readonly_env = os.environ.get('VERCEL', False)
                
                if not readonly_env:
                    # For traditional deployments - update settings.py file
                    settings_path = settings.BASE_DIR / 'modular_django' / 'settings.py'
                    with open(settings_path, 'r') as f:
                        content = f.read()
                    
                    # Remove from INSTALLED_APPS
                    new_content = content.replace(f'    "{module_name}",\n', '')
                    new_content = new_content.replace(f"    '{module_name}',\n", '')
                    
                    with open(settings_path, 'w') as f:
                        f.write(new_content)
                
                # Update module status in database (this works in both environments)
                module.installed = False
                module.active = False
                module.save()
                
                messages.success(request, _(f"Module {module.name} uninstalled successfully."))
                
                if readonly_env:
                    messages.info(request, _("You'll need to restart the application for the changes to take effect."))
                    
                return redirect('module_list')
            
            except Exception as e:
                messages.error(request, _(f"Failed to uninstall module: {str(e)}"))
        else:
            return redirect('module_list')
    
    return render(request, 'module_engine/confirm_uninstall.html', {
        'module': module
    })