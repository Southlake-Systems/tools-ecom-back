# Deploying the Yessare API

Stack: Django + Gunicorn, Celery worker, Postgres, Redis, nginx (TLS + static/media),
all via `docker compose`. Domain: **api.yessaretools.com**.

## 1. Prerequisites
- A host with Docker + Docker Compose plugin.
- DNS `A` record: `api.yessaretools.com` → host IP.
- Ports 80 and 443 open.

## 2. Configure
```bash
cp .env.example .env
# edit .env: SECRET_KEY (long random), DB_USER/DB_PASSWORD/DB_NAME, USE_S3 if applicable
```
`DB_HOST`, `DB_PORT` and `CELERY_BROKER_URL` are set automatically by `docker-compose.yml`
(to `db` / `redis`), so leave the `.env` defaults.

## 3. First run (obtain TLS cert)
```bash
mkdir -p deploy/certbot/www deploy/certbot/conf

# temporarily use the HTTP-only vhost so nginx starts without certs
sed -i 's#api.yessaretools.com.conf#api.yessaretools.com.http-only.conf#' docker-compose.yml

docker compose up -d --build db redis web nginx

docker run --rm \
  -v "$PWD/deploy/certbot/conf:/etc/letsencrypt" \
  -v "$PWD/deploy/certbot/www:/var/www/certbot" \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d api.yessaretools.com --email you@example.com --agree-tos --no-eff-email

# switch back to the TLS vhost
sed -i 's#api.yessaretools.com.http-only.conf#api.yessaretools.com.conf#' docker-compose.yml
docker compose up -d
```

## 4. Normal operation
```bash
docker compose up -d --build          # deploy / redeploy
docker compose exec web python manage.py createsuperuser
docker compose logs -f web worker
```
- Migrations run automatically on the `web` container (`RUN_MIGRATIONS=1`).
- `collectstatic` runs at image build time; `static` + `media` are shared volumes that
  nginx serves directly.

## 5. Cert renewal (cron on the host)
```
0 3 * * * cd /opt/yessare-api && docker run --rm \
  -v "$PWD/deploy/certbot/conf:/etc/letsencrypt" \
  -v "$PWD/deploy/certbot/www:/var/www/certbot" \
  certbot/certbot renew --quiet && docker compose exec nginx nginx -s reload
```

## Notes
- Auth is JWT (`Authorization: Bearer …`) — no session cookies cross domains, so no CSRF
  wiring is needed for the API. `CSRF_TRUSTED_ORIGINS` / `SECURE_PROXY_SSL_HEADER` in
  `config/settings.py` cover the Django admin at `api.yessaretools.com/admin/`.
- To use an external managed Postgres instead of the `db` service: remove `db` from
  `docker-compose.yml`, set `DB_HOST`/`DB_PORT`/credentials in `.env`, and drop the
  `DB_HOST: db` override on `web` and `worker`.
