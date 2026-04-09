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
- **Deployment**: Ready for Heroku/Gunicorn

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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.local.example .env.local  # Create from template
   # Edit .env.local with your settings
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

1. Set `DJANGO_ENV=production` in environment
2. Use `.env.prod` for production settings
3. Run `python manage.py collectstatic`
4. Deploy with Gunicorn/WhiteNoise

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