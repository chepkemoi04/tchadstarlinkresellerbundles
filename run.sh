#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export DJANGO_DEBUG="${DJANGO_DEBUG:-true}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-localhost,127.0.0.1,0.0.0.0}"
python manage.py migrate
exec python manage.py runserver "${HOST:-0.0.0.0}:${PORT:-8000}"
