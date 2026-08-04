from django.conf import settings
from core.utils import get_wedding_datetime


def wedding_settings(request):
    # Expose the wedding moment as an ISO 8601 string including the timezone
    # offset so client-side JS interprets the same absolute instant.
    return {
        'WEDDING_DATE': get_wedding_datetime().isoformat(),
    }