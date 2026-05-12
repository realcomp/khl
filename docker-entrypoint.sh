#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
# A simple wait-for-it for postgres using python socket
python -c "
import socket
import time
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('db', 5432))
        s.close()
        break
    except Exception:
        time.sleep(1)
"
echo "PostgreSQL started"

echo "Waiting for Redis..."
python -c "
import socket
import time
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('redis', 6379))
        s.close()
        break
    except Exception:
        time.sleep(1)
"
echo "Redis started"

# Note: Django 1.7 doesn't support --noinput in the same way, but usually it works.
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
# Ignore errors on collectstatic if some bowers are missing
python manage.py collectstatic --noinput || true

exec "$@"
