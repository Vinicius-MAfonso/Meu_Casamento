# Meu Casamento - Django Wedding RSVP System

A beautiful Django-based wedding RSVP system with guest management, confirmation tracking, and responsive design.

## Features

- **Guest Group Management**: Organize guests into groups with unique access codes
- **RSVP System**: Secure confirmation system with real-time updates
- **Admin Interface**: Comprehensive admin panel for managing guests and groups
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS
- **Countdown Timer**: Live wedding countdown
- **Calendar Integration**: Save-the-date links for Google Calendar and Apple Calendar

## Tech Stack

- **Backend**: Django 5.2.8
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Gunicorn + Nginx on a Linux server, or Render

## Setup

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Meu_Casamento
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies (includes dev-only tooling like django-browser-reload;
   production installs use `requirements.txt` alone -- see `build.sh`):
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.local.example .env.local  # Create from template
   # Edit .env.local with your settings -- at minimum set SECRET_KEY.
   # ALLOWED_HOSTS must include localhost,127.0.0.1 or `runserver` will
   # reject every request with DisallowedHost.
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Build static files:
   ```bash
   python manage.py tailwind install
   python manage.py tailwind build
   ```

### Development

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. For Tailwind CSS watching:
   ```bash
   python manage.py tailwind start
   ```

### Production Deployment

The project is ready for either Render or a traditional Linux server such as EC2.

#### Render

1. In the Render Dashboard, create a **Web Service** from this repo:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn meu_casamento.wsgi:application`
2. Set environment variables (Settings → Environment): `DJANGO_ENV=production`,
   `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` (your custom domain or hostname),
   and `DATABASE_URL`.
3. `build.sh` installs dependencies, builds Tailwind CSS, creates the shared cache table,
   runs `collectstatic`, and runs `migrate`.

#### EC2 / Linux server

1. Create a production environment file such as `.env.prod` with at least `DJANGO_ENV`,
   `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CACHE_BACKEND=database`, and
   `DATABASE_URL`.
2. Install dependencies and run the same build steps as in `build.sh`.
3. Run Gunicorn behind Nginx on `127.0.0.1:8000` (or a Unix socket), not directly on the public network.
4. Use a systemd service and an Nginx reverse proxy with TLS termination.
   Example files are available in the `deploy/` directory.
5. For the service, prefer an environment file outside the repository, for example
   `/etc/meu-casamento/.env.prod` with `chmod 600`, instead of putting secrets in the
   systemd unit itself.
6. For certificate issuance, start with the HTTP-only config in `deploy/nginx-http.conf`,
   obtain the certificate with `certbot --nginx`, and then switch to the HTTPS config in
   `deploy/nginx-meu-casamento.conf`.
7. Enable the service after copying the unit file:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now meu-casamento
   sudo nginx -t && sudo systemctl reload nginx
   ```

`Procfile.tailwind` is for **local development only** (runs `runserver` and
the Tailwind watcher together via `honcho`/`foreman`). Never point production
traffic at `manage.py runserver`.

## Usage

### Admin Panel

Access `/admin/` to manage groups and guests.

### Guest RSVP

Guests access their RSVP page via unique URLs like `/<uuid>/` where `<uuid>` is their group's access code.

## Configuration

Key settings in `meu_casamento/settings.py`:

- `WEDDING_DATE`: Wedding date in ISO format (YYYY-MM-DDTHH:MM:SS)
- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable/disable debug mode

## Testing

Run tests with:
```bash
python manage.py test
```

## License

This project is private and proprietary.