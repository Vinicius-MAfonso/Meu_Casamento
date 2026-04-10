import json
import logging
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_safe
from .models import Convidado, Grupo
from django.core.cache import cache
import time


logger = logging.getLogger(__name__)


def home(request, codigo_acesso):
    grupo = get_object_or_404(Grupo, codigo_acesso=codigo_acesso)
    convidados = Convidado.objects.filter(grupo=grupo)

    return render(request, "core/home.html", {"grupo": grupo, "convidados": convidados})


def rate_limit_ip(request, max_requests=5, window=60):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    
    cache_key = f"ratelimit_{ip}"
    requests = cache.get(cache_key, [])
    now = time.time()

    requests = [req_time for req_time in requests if now - req_time < window]

    if len(requests) >= max_requests:
        return False

    requests.append(now)
    cache.set(cache_key, requests, window)
    return True


@require_POST
def api_confirmar_presenca(request, codigo_acesso):
    try:
        if not rate_limit_ip(request):
            return JsonResponse(
                {"success": False, "error": "Muitas tentativas. Aguarde um momento."},
                status=429,
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON received for group {codigo_acesso}")
            return JsonResponse(
                {"success": False, "error": "Formato de dados inválido"}, status=400
            )
        
        ids_confirmados = data.get("confirmacao", [])

        grupo = get_object_or_404(Grupo, codigo_acesso=codigo_acesso)
        if grupo.status_confirmacao:
            return JsonResponse(
                {"success": False, "error": "Presença já foi confirmada"}, status=400
            )
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
        return JsonResponse(
            {"success": False, "error": "Erro interno do servidor"}, status=500
        )


@require_safe
def api_status_projeto(request):
    return HttpResponse('{"status": "ok"}', content_type="application/json", status=200)
