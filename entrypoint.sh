#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/src/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm myproj.wsgi:application --bind "0.0.0.0:${APP_PORT}"