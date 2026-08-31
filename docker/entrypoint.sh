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

    # Bootstrap a superuser if DJANGO_SUPERUSER_USERNAME/PASSWORD are set.
    # Idempotent: creates the user once, otherwise resets its password.
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Ensuring superuser '$DJANGO_SUPERUSER_USERNAME'..."
        python manage.py shell <<'PYEOF'
import os
from django.contrib.auth import get_user_model

U = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

user, created = U.objects.get_or_create(
    username=username,
    defaults={"email": email},
)
user.is_staff = True
user.is_superuser = True
if email:
    user.email = email
user.set_password(password)
user.save()
print("created" if created else "updated", "superuser", username)
PYEOF
    fi
fi

exec "$@"
