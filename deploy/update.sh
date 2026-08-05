set -euo pipefail

APP_DIR=${APP_DIR:-/srv/meu-casamento}
APP_USER=${APP_USER:-meucasamento}
APP_GROUP=${APP_GROUP:-$APP_USER}
BRANCH=${BRANCH:-main}
SERVICE_NAME=${SERVICE_NAME:-meu-casamento}

if [[ $EUID -ne 0 ]]; then
  echo "Run as root (sudo ./deploy/update.sh)." >&2
  exit 1
fi

if [[ ! -d "$APP_DIR/.git" ]]; then
  echo "Didn't find a git clone in $APP_DIR. Run ec2-bootstrap.sh first." >&2
  exit 1
fi

echo "==> Searching for new code ($BRANCH)..."
sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && git fetch --all --prune && git checkout '$BRANCH' && git pull --ff-only origin '$BRANCH'"

echo "==> Installing dependencies..."
sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && ./.venv/bin/pip install -r requirements.txt"

echo "==> Build and migrations..."
sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && set -a && . /etc/meu-casamento/.env.prod && set +a && \
  ./.venv/bin/python3 manage.py tailwind install && \
  ./.venv/bin/python3 manage.py tailwind build && \
  ./.venv/bin/python3 manage.py createcachetable && \
  ./.venv/bin/python3 manage.py collectstatic --no-input && \
  ./.venv/bin/python3 manage.py migrate"

echo "==> Restarting $SERVICE_NAME..."
systemctl restart "$SERVICE_NAME"
systemctl status "$SERVICE_NAME" --no-pager -l | head -n 10

echo "==> Update applied."
