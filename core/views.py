import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_safe
from .models import Convidado, Grupo

logger = logging.getLogger(__name__)


def home(request, codigo_acesso):
    grupo = get_object_or_404(Grupo, codigo_acesso=codigo_acesso)
    convidados = Convidado.objects.filter(grupo=grupo)

    return render(request, "core/home.html", {"grupo": grupo, "convidados": convidados})


@require_POST
def api_confirmar_presenca(request, codigo_acesso):
    try:
        data = json.loads(request.body)
        ids_confirmados = data.get("confirmacao", [])

        grupo = get_object_or_404(Grupo, codigo_acesso=codigo_acesso)
        convidados = Convidado.objects.filter(grupo=grupo)

        for convidado in convidados:
            if str(convidado.id) in ids_confirmados:
                convidado.status_confirmacao = "confirmado"
            else:
                convidado.status_confirmacao = "pendente"
            convidado.save()

        grupo.status_confirmacao = True
        grupo.save()

        return JsonResponse(
            {"success": True, "message": "Presença confirmada com sucesso!"}
        )

    except Exception as e:
        logger.error(f"Error confirming presence for group {codigo_acesso}: {str(e)}")
        return JsonResponse({"success": False, "error": "Erro interno do servidor"}, status=500)

@require_safe
def api_status_projeto(request):
    return HttpResponse('{"status": "ok"}', content_type='application/json', status=200)
