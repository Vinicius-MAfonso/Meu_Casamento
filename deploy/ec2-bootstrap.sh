#!/usr/bin/env bash
set -euo pipefail

APP_DIR=${APP_DIR:-/srv/meu-casamento}
APP_USER=${APP_USER:-meucasamento}
APP_GROUP=${APP_GROUP:-$APP_USER}
DOMAIN=${DOMAIN:-meucasamento.example.com}
EMAIL=${EMAIL:-admin@$DOMAIN}
ENABLE_SSL=${ENABLE_SSL:-true}
REPO_URL=${REPO_URL:-https://github.com/your-user/Meu_Casamento.git}
BRANCH=${BRANCH:-main}
REPO_SOURCE_DIR=${REPO_SOURCE_DIR:-}
SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 48 | tr -d '\n')}
POSTGRES_DB=${POSTGRES_DB:-meu_casamento}
POSTGRES_USER=${POSTGRES_USER:-meu_casamento}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-$(openssl rand -base64 24 | tr -d '\n')}
DATABASE_URL=${DATABASE_URL:-postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/$POSTGRES_DB}
ALLOWED_HOSTS=${ALLOWED_HOSTS:-$DOMAIN,localhost,127.0.0.1}

if [[ $EUID -ne 0 ]]; then
  echo "Run this script as root (or with sudo)." >&2
  exit 1
fi

if [[ -z "$REPO_SOURCE_DIR" ]]; then
  if [[ -f "$PWD/manage.py" ]]; then
    REPO_SOURCE_DIR="$PWD"
  else
    REPO_SOURCE_DIR=""
  fi
fi

if [[ -n "$REPO_SOURCE_DIR" && ! -f "$REPO_SOURCE_DIR/manage.py" ]]; then
  echo "The provided source directory does not look like a Django project: $REPO_SOURCE_DIR" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y \
  python3 python3-pip python3-venv python3-dev build-essential libpq-dev \
  nginx git curl certbot python3-certbot-nginx nodejs npm rsync postgresql postgresql-contrib ufw sudo

if ! id "$APP_USER" >/dev/null 2>&1; then
  useradd --system --create-home --shell /bin/bash "$APP_USER"
fi

install -d -o "$APP_USER" -g "$APP_GROUP" -m 755 "$APP_DIR" /etc/meu-casamento /var/log/meu-casamento
install -d -o "$APP_USER" -g "$APP_GROUP" -m 755 /var/log/meu-casamento/gunicorn

if [[ -n "$REPO_SOURCE_DIR" ]]; then
  if [[ "$REPO_SOURCE_DIR" != "$APP_DIR" ]]; then
    rsync -a --delete "$REPO_SOURCE_DIR/" "$APP_DIR/"
  fi
else
  if [[ -d "$APP_DIR/.git" ]]; then
    sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && git fetch --all --prune && git checkout '$BRANCH' && git pull --ff-only origin '$BRANCH'"
  elif [[ -d "$APP_DIR" && -n "$(find "$APP_DIR" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    echo "The application directory exists and is not empty: $APP_DIR" >&2
    echo "Please remove it or point APP_DIR to a clean directory." >&2
    exit 1
  else
    sudo -u "$APP_USER" bash -lc "git clone --branch '$BRANCH' '$REPO_URL' '$APP_DIR'"
  fi
fi

chown -R "$APP_USER":"$APP_GROUP" "$APP_DIR"

service postgresql start || true
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'" | grep -q 1 || sudo -u postgres psql -c "CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;"

cat > /etc/meu-casamento/.env.prod <<EOF
DJANGO_ENV=production
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$ALLOWED_HOSTS
CACHE_BACKEND=database
DATABASE_URL=$DATABASE_URL
EOF

install -o "$APP_USER" -g "$APP_GROUP" -m 640 /etc/meu-casamento/.env.prod /etc/meu-casamento/.env.prod
ln -sfn /etc/meu-casamento/.env.prod "$APP_DIR/.env.prod"
chown -R "$APP_USER":"$APP_GROUP" "$APP_DIR"
chown "$APP_USER":"$APP_GROUP" /etc/meu-casamento/.env.prod

sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && python3 -m venv .venv && ./.venv/bin/pip install --upgrade pip setuptools wheel && ./.venv/bin/pip install -r requirements.txt"

cp "$APP_DIR/deploy/meu-casamento.service" /etc/systemd/system/meu-casamento.service
sed -i "s/^User=.*/User=$APP_USER/" /etc/systemd/system/meu-casamento.service
sed -i "s/^Group=.*/Group=$APP_GROUP/" /etc/systemd/system/meu-casamento.service
cp "$APP_DIR/deploy/nginx-http.conf" /etc/nginx/sites-available/meu-casamento
sed -i "s/meucasamento.example.com/$DOMAIN/g" /etc/nginx/sites-available/meu-casamento
ln -sfn /etc/nginx/sites-available/meu-casamento /etc/nginx/sites-enabled/meu-casamento
rm -f /etc/nginx/sites-enabled/default

ufw --force enable
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw status verbose || true

nginx -t
systemctl restart nginx

sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && set -a && . /etc/meu-casamento/.env.prod && set +a && ./.venv/bin/python3 manage.py tailwind install && ./.venv/bin/python3 manage.py tailwind build && ./.venv/bin/python3 manage.py createcachetable --noinput && ./.venv/bin/python3 manage.py collectstatic --no-input && ./.venv/bin/python3 manage.py migrate"

systemctl daemon-reload
systemctl enable --now meu-casamento

mkdir -p /etc/systemd/system/meu-casamento.service.d
cat > /etc/systemd/system/meu-casamento.service.d/override.conf <<EOF
[Service]
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/meu-casamento /var/log/meu-casamento
EOF

systemctl daemon-reload
systemctl restart meu-casamento

if [[ "$ENABLE_SSL" == "true" ]]; then
  if certbot --nginx --non-interactive --agree-tos --email "$EMAIL" -d "$DOMAIN"; then
    cp "$APP_DIR/deploy/nginx-meu-casamento.conf" /etc/nginx/sites-available/meu-casamento
    sed -i "s/meucasamento.example.com/$DOMAIN/g" /etc/nginx/sites-available/meu-casamento
    ln -sfn /etc/nginx/sites-available/meu-casamento /etc/nginx/sites-enabled/meu-casamento
    nginx -t
    echo "SSL certificate installed successfully."
  else
    echo "Certbot could not finish TLS setup automatically. Check DNS and port 80/443, then run:"
    echo "  sudo certbot --nginx -d $DOMAIN"
  fi
fi

systemctl restart meu-casamento
systemctl reload nginx

echo "Bootstrap complete."
echo "Check status with: sudo systemctl status meu-casamento"
echo "And verify the site at https://$DOMAIN"
