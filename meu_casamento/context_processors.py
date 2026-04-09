from django.conf import settings

def wedding_settings(request):
    return {
        'WEDDING_DATE': settings.WEDDING_DATE,
    }