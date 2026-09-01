from django.contrib import admin
from django.urls import path, include
from django.conf import settings

admin_path = getattr(settings, "DJANGO_ADMIN_URL", "admin/").strip("/")
admin_url = f"{admin_path}/" if admin_path else "admin/"

urlpatterns = [
    path(admin_url, admin.site.urls),
    path('', include('core.urls'))
]
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]