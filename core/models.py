import uuid
from django.db import models

class Grupo(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome do Grupo")
    status_confirmacao = models.BooleanField(verbose_name="Status de confirmação do grupo", default=False)
    codigo_acesso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return f"Grupo: {self.nome} ({self.codigo_acesso})"

class Convidado(models.Model):
    CONFIRMACAO = [
        ("confirmado", "Confirmado"),
        ("pendente", "Pendente"),
    ]
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="convidados")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    is_representante = models.BooleanField(verbose_name="É líder/representante?")
    status_confirmacao = models.CharField(max_length=50, verbose_name="Status de presença", choices=CONFIRMACAO, default="pendente")
    def __str__(self):
        return f"Convidado: {self.nome} (Grupo: {self.grupo.nome})"