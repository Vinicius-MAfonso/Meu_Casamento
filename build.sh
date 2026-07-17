set -o errexit

pip install -r requirements.txt

mkdir -p logs

tailwindcss -i theme/static_src/src/styles.css -o theme/static/css/dist/styles.css --minify

python manage.py collectstatic --noinput

python manage.py migrate