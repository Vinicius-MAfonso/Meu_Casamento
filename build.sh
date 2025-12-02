#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

tailwindcss -i theme/static_src/src/styles.css -o theme/static/css/dist/styles.css --minify

# Collect static files for production
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate