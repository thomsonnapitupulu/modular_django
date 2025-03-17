#!/bin/bash

# Use the Python that Vercel provides
echo "Python location: $(which python3)"

# Install dependencies
python3 -m pip install -r requirements.txt

# Create static directories
mkdir -p static staticfiles

# Make migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Optional: Create superuser (you might want to handle this differently)
# export DJANGO_SUPERUSER_PASSWORD=your_password
# export DJANGO_SUPERUSER_EMAIL=admin@example.com
# export DJANGO_SUPERUSER_USERNAME=admin
# python manage.py createsuperuser --noinput || true