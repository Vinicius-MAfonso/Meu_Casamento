from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("<uuid:codigo_acesso>/", views.home, name="home"),
    path(
        "api/confirmar/<uuid:codigo_acesso>/", views.api_confirmar_presenca, name="api_confirmar"
    ),
]
