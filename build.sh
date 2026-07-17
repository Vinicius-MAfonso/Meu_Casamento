#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py tailwind install --no-input
python manage.py tailwind build --no-input

python manage.py collectstatic --no-input

python manage.py migrate