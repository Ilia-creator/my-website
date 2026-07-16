#!/bin/sh
set -e

echo "Running collectstatic..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate --no-input

echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 mysite.wsgi:application --access-logfile - --error-logfile -
