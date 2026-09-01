#!/bin/bash
set -e

echo "Buildando Tailwind CSS..."
python manage.py tailwind build

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Criando tabela de cache (se não existir)..."
python manage.py createcachetable

echo "Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo "Iniciando Gunicorn..."
exec gunicorn meu_casamento.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120



