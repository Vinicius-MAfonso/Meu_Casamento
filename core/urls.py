from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path('<uuid:codigo_acesso>/', views.home, name='home'),
]
