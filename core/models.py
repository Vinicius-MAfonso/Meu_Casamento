import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse


class Grupo(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome do Grupo")
    status_confirmacao = models.BooleanField(
        verbose_name="Status de confirmação do grupo", default=False
    )
    codigo_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    encurtador_url = models.URLField(
        max_length=200, verbose_name="Encurtador de URL", blank=True, null=True
    )

    def __str__(self):
        return f"{self.nome} ({self.codigo_acesso})"

    def get_absolute_url(self):
        return reverse("core:home", kwargs={"codigo_acesso": self.codigo_acesso})

    @property
    def full_url(self):
        base_url = getattr(settings, "SITE_URL", "").rstrip("/")
        return f"{base_url}{self.get_absolute_url()}"


class Convidado(models.Model):
    grupo = models.ForeignKey(
        Grupo, on_delete=models.CASCADE, related_name="convidados"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    status_confirmacao = models.BooleanField(
        verbose_name="Status de confirmação do Convidado", default=False
    )

    def __str__(self):
        return f"{self.nome} (Grupo: {self.grupo.nome})"
