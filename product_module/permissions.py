# product_module/permissions.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Role definitions
ROLES = {
    'manager': {
        'can_view': True,
        'can_add': True,
        'can_change': True,
        'can_delete': True,
    },
    'user': {
        'can_view': True,
        'can_add': True,
        'can_change': True,
        'can_delete': False,
    },
    'public': {
        'can_view': True,
        'can_add': False,
        'can_change': False,
        'can_delete': False,
    }
}

def setup_permissions():
    """Set up the permissions for the product module."""
    # Get the content type for the Product model
    Product = apps.get_model('product_module', 'Product')
    content_type = ContentType.objects.get_for_model(Product)
    
    # Create or get the groups
    manager_group, _ = Group.objects.get_or_create(name='product_manager')
    user_group, _ = Group.objects.get_or_create(name='product_user')
    public_group, _ = Group.objects.get_or_create(name='product_public')
    
    # Clear existing permissions for these groups
    manager_group.permissions.clear()
    user_group.permissions.clear()
    public_group.permissions.clear()
    
    # Get permissions - handle case where they might not exist yet
    perms = {}
    for perm_name in ['view', 'add', 'change', 'delete']:
        perm_codename = f'{perm_name}_product'
        try:
            perm = Permission.objects.get(codename=perm_codename, content_type=content_type)
            perms[f'can_{perm_name}'] = perm
        except Permission.DoesNotExist:
            # Permission doesn't exist yet, we'll handle this later
            continue
    
    # Skip assigning permissions if they don't exist yet
    if not perms:
        print("Permissions for Product model not found. Will be set up after migrations.")
        return
    
    # Manager permissions
    for perm_key, allowed in ROLES['manager'].items():
        if allowed and perm_key in perms:
            manager_group.permissions.add(perms[perm_key])
    
    # User permissions
    for perm_key, allowed in ROLES['user'].items():
        if allowed and perm_key in perms:
            user_group.permissions.add(perms[perm_key])
    
    # Public permissions
    for perm_key, allowed in ROLES['public'].items():
        if allowed and perm_key in perms:
            public_group.permissions.add(perms[perm_key])


def has_product_permission(user, permission_type):
    """Check if a user has permission for product operations."""
    if user.is_superuser:
        return True
    
    # Check group permissions
    if user.groups.filter(name='product_manager').exists():
        return ROLES['manager'].get(permission_type, False)
    
    if user.groups.filter(name='product_user').exists():
        return ROLES['user'].get(permission_type, False)
    
    # Default to public permissions for authenticated users without specific groups
    if user.is_authenticated:
        return ROLES['public'].get(permission_type, False)
    
    return False


# Define a separate post_migrate receiver
@receiver(post_migrate)
def create_permissions_after_migrate(sender, **kwargs):
    """
    Create permissions after migrations are done.
    This runs after all models are created and permissions are available.
    """
    # Only run for product_module app
    if sender.name != 'product_module':
        return
    
    # Now permissions should exist, so we can set them up
    setup_permissions()