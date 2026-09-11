import logging
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_wedding_datetime():
    """Parse settings.WEDDING_DATE into an aware datetime in the project's TIME_ZONE."""
    naive_or_aware = datetime.fromisoformat(settings.WEDDING_DATE)
    if timezone.is_naive(naive_or_aware):
        return timezone.make_aware(naive_or_aware)
    return naive_or_aware


def get_rsvp_deadline():
    """The moment RSVPs stop being accepted -- settings.RSVP_CLOSE_DAYS_BEFORE days
    before the wedding, in the site's configured timezone."""
    return get_wedding_datetime() - timedelta(days=settings.RSVP_CLOSE_DAYS_BEFORE)


def is_rsvp_closed():
    return timezone.now() >= get_rsvp_deadline()


def shorten_url_tinyurl(url: str, timeout: int = 5) -> str:
    api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url, safe='')}"
    req = urllib.request.Request(
        api_url,
        headers={"User-Agent": "MeuCasamento/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8").strip()
