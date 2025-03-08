# Modular Django Application

A flexible Django application with a module system for dynamically installing, upgrading, and uninstalling feature modules.

## Features

- **Module Management System**: Install, upgrade, and uninstall modules dynamically
- **Role-Based Access Control**: Different permission levels (Manager, User, Public)
- **Example Product Module**: Complete CRUD operations with permission controls
- **Schema Change Management**: Handle database changes through the upgrade process

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Module Engine](#module-engine)
- [Product Module](#product-module)
- [Use Cases](#use-cases)
  - [Installing a Module](#installing-a-module)
  - [Upgrading a Module](#upgrading-a-module)
  - [Uninstalling a Module](#uninstalling-a-module)
  - [Managing Products](#managing-products)
- [Role-Based Access](#role-based-access)
- [Custom Module Development](#custom-module-development)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- pip

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modular_django.git
   cd modular_django
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations for the core system:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Register the Product Module in the database:
   ```bash
   python manage.py shell
   ```
   
   In the Python shell:
   ```python
   from module_engine.models import Module
   
   # Create the module entry
   Module.objects.create(
       name="Product Management",
       identifier="product_module",
       version="1.0.0",
       installed=False,
       active=False
   )
   
   # Verify it was created
   print(Module.objects.all())
   
   # Exit the shell
   exit()
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Project Structure

```
modular_django/
├── manage.py
├── modular_django/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── module_engine/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── module_engine/
│   │       ├── index.html
│   │       ├── install.html
│   │       └── confirm_uninstall.html
│   └── management/
│       └── commands/
│           ├── install_module.py
│           ├── upgrade_module.py
│           └── uninstall_module.py
└── product_module/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── forms.py
    ├── permissions.py
    ├── module_info.py
    ├── migrations/
    │   └── __init__.py
    └── templates/
        └── product_module/
            ├── index.html
            ├── product_list.html
            ├── product_detail.html
            ├── product_form.html
            └── confirm_delete.html
```

## Module Engine

The module engine is the core of the application, responsible for managing modules. It provides:

- A web interface for module management
- Backend systems for installing, upgrading, and uninstalling modules
- Database tracking of module status and versions

Access the module manager at: http://127.0.0.1:8000/modules/

## Product Module

The product module is an example module that demonstrates the system's capabilities:

- Product CRUD operations (Create, Read, Update, Delete)
- Role-based access control
- Form validation
- Confirmation dialogs for destructive operations

Once installed, access the product module at: http://127.0.0.1:8000/products/

## Use Cases
![Screenshot](screenshots/confirm_install_module.png?raw=true)
### Installing a Module

1. Log in as an admin user
2. Navigate to the Module Manager (http://127.0.0.1:8000/modules/)
3. In the list of available modules, find the "Product Management" module
4. Click the "Install" button
5. Confirm the installation on the confirmation page
6. The system will:
   - Add the module to INSTALLED_APPS
   - Run necessary migrations
   - Mark the module as installed
7. Upon success, you'll be redirected to the module list with a success message

If you encounter migration errors, try manually running:
```bash
python manage.py makemigrations product_module
python manage.py migrate product_module
```

### Upgrading a Module

When a module needs to be updated (e.g., adding a new field):

1. Log in as an admin user
2. Navigate to the Module Manager
3. Find the installed module you want to upgrade
4. Click the "Upgrade" button
5. Confirm the upgrade on the confirmation page
6. The system will:
   - Check for schema changes
   - Generate and apply migrations if needed
   - Update the module version

Example of adding a field to the Product model:

1. Edit `product_module/models.py` to add a new field
2. Update the version in `product_module/module_info.py`
3. Use the upgrade process to apply the changes

### Uninstalling a Module

1. Log in as an admin user
2. Navigate to the Module Manager
3. Find the installed module you want to remove
4. Click the "Uninstall" button
5. Confirm the uninstallation (two confirmation steps for safety)
6. The system will:
   - Remove the module from INSTALLED_APPS
   - Mark the module as uninstalled
   - Unregister module URLs

**Note**: Uninstalling does not delete data from the database, it only makes the module inaccessible.

### Managing Products

#### Viewing Products

1. Navigate to the Products page (http://127.0.0.1:8000/products/)
2. Click "View Products" to see the product list
3. All users can view the product list, but available actions depend on roles

#### Creating a Product

1. Navigate to the Products list
2. Click "Add New Product" (available for Manager and User roles)
3. Fill in the product details:
   - Name
   - Barcode (must be unique)
   - Price (must be greater than zero)
   - Stock (must not be negative)
4. Click "Save" to create the product
5. Upon success, you'll be redirected to the product list

#### Updating a Product

1. Navigate to the Products list
2. Click "View" on a product to see its details
3. Click "Edit" (available for Manager and User roles)
4. Modify the product details
5. Click "Save" to update the product
6. Upon success, you'll be redirected to the product details page

#### Deleting a Product

1. Navigate to the Products list
2. Click "View" on a product to see its details
3. Click "Delete" (available only for Manager role)
4. Confirm the deletion in the confirmation dialog
5. Upon confirmation, the product will be deleted
6. You'll be redirected to the product list

## Role-Based Access

The system includes three predefined roles with different access levels:

### Manager Role

- Can view all products
- Can create new products
- Can edit existing products
- Can delete products

### User Role

- Can view all products
- Can create new products
- Can edit existing products
- Cannot delete products

### Public Role

- Can view all products
- Cannot create new products
- Cannot edit existing products
- Cannot delete products

### Assigning Roles

To assign a role to a user:

1. Log in as an admin
2. Go to the Django admin interface (http://127.0.0.1:8000/admin/)
3. Navigate to Users
4. Select a user
5. In the "Groups" section, add the user to the appropriate group:
   - product_manager
   - product_user
   - product_public

## Custom Module Development

To create your own module:

1. Create a new Django app:
   ```bash
   python manage.py startapp your_module_name
   ```

2. Add a `module_info.py` file:
   ```python
   MODULE_INFO = {
       'name': 'Your Module Name',
       'identifier': 'your_module_name',
       'version': '1.0.0',
       'description': 'Description of your module',
       'author': 'Your Name',
       'url_prefix': 'your-url-prefix',
   }
   ```

3. Implement your models, views, forms, and templates

4. Register your module in the database:
   ```python
   from module_engine.models import Module
   
   Module.objects.create(
       name="Your Module Name",
       identifier="your_module_name",
       version="1.0.0",
       installed=False,
       active=False
   )
   ```

5. Install your module through the module manager

## Troubleshooting

### Module Not Appearing in List

Make sure you've registered the module in the database using the shell command provided in the installation steps.

### Installation Fails with Migration Errors

1. Check the error message for specific details
2. Ensure your models are properly defined
3. Try running migrations manually:
   ```bash
   python manage.py makemigrations your_module_name
   python manage.py migrate your_module_name
   ```

### Permission Issues

1. Make sure users are assigned to the correct groups
2. Check that the module's permissions are properly set up
3. Ensure the `post_migrate` signal is properly connecting to the `setup_permissions` function

### Module URL Not Accessible After Installation

1. Check that the module is marked as installed and active in the database
2. Verify that the module is added to INSTALLED_APPS
3. Restart the Django server to refresh the URL configurations
