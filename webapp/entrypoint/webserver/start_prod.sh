#!/usr/bin/env bash

set -e

echo "==> loading secrets..."
./config/load_secrets.sh

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Collecting statics..."
python manage.py collectstatic --noinput -v 2

echo "==> Running server..."
exec gunicorn -c /app/config/gunicorn.conf.py vehiclesapi.wsgi:application
