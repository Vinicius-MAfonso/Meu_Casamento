#!/usr/bin/env bash
set -euo pipefail

# Backup script for Meu_Casamento Postgres database.
# Expects /etc/meu-casamento/.env.prod to exist with DATABASE_URL or
# POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB variables.

BACKUP_DIR=/var/backups/meu-casamento
mkdir -p "$BACKUP_DIR"

if [[ -f /etc/meu-casamento/.env.prod ]]; then
  set -a
  # shellcheck disable=SC1091
  . /etc/meu-casamento/.env.prod
  set +a
fi

TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
FILENAME="$BACKUP_DIR/meu-casamento-$TIMESTAMP.dump"

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Starting backup to $FILENAME"

if [[ -n "${DATABASE_URL:-}" ]]; then
  PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_dump --dbname="$DATABASE_URL" -Fc -f "$FILENAME"
else
  PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_dump -h localhost -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-meu_casamento}" -Fc -f "$FILENAME"
fi

chown -R meucasamento:meucasamento "$BACKUP_DIR" || true
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Backup completed"
