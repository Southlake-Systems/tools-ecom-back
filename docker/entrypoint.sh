#!/bin/sh
set -e

# Wait for the database if DB_HOST/DB_PORT are set.
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
    until python -c "import socket,sys; s=socket.socket(); s.settimeout(2); \
        sys.exit(0) if s.connect_ex(('$DB_HOST', int('${DB_PORT:-5432}')))==0 else sys.exit(1)" 2>/dev/null; do
        sleep 1
    done
    echo "Database is up."
fi

# Only the web container should run migrations (RUN_MIGRATIONS=1).
if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
    echo "Running migrations..."
    python manage.py migrate --noinput
fi

exec "$@"
