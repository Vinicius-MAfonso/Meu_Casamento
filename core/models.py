import secrets
import string
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse

SHORT_CODE_CHARACTERS = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"


def generate_short_code(length=6):
    return "".join(secrets.choice(SHORT_CODE_CHARACTERS) for _ in range(length))


class Grupo(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome do Grupo")
    status_confirmacao = models.BooleanField(
        verbose_name="Status de confirmação do grupo", default=False
    )
    codigo_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    codigo_curto = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Código Curto",
    )
    encurtador_url = models.URLField(
        max_length=200, verbose_name="Encurtador de URL", blank=True, null=True
    )

    def __str__(self):
        return f"{self.nome} ({self.codigo_acesso})"

    def get_absolute_url(self):
        return reverse("core:home", kwargs={"codigo_acesso": self.codigo_acesso})

    def get_full_url(self, request=None):
        url_path = self.get_absolute_url()
        if request:
            host = request.get_host()
            if "localhost" not in host and "127.0.0.1" not in host:
                return request.build_absolute_uri(url_path)
        base_url = getattr(settings, "SITE_URL", "").rstrip("/")
        return f"{base_url}{url_path}"

    @property
    def full_url(self):
        return self.get_full_url()

    def get_short_url(self, request=None):
        if not self.codigo_curto:
            return ""
        short_path = reverse("core:short_redirect", kwargs={"codigo_curto": self.codigo_curto})
        if request:
            host = request.get_host()
            if "localhost" not in host and "127.0.0.1" not in host:
                return request.build_absolute_uri(short_path)
        base_url = getattr(settings, "SITE_URL", "").rstrip("/")
        return f"{base_url}{short_path}"

    @property
    def short_url(self):
        return self.get_short_url()

    def ensure_unique_short_code(self):
        if not self.codigo_curto:
            while True:
                candidate = generate_short_code()
                if not Grupo.objects.filter(codigo_curto=candidate).exists():
                    self.codigo_curto = candidate
                    break

    def save(self, *args, **kwargs):
        self.ensure_unique_short_code()
        # Keep encurtador_url in sync with the native short link
        self.encurtador_url = self.short_url
        super().save(*args, **kwargs)


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
