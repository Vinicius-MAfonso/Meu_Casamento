from django.shortcuts import render, redirect
from .models import Convidado, Grupo

def home(request, codigo_acesso):
    if request.method == 'POST':
        grupo = Grupo.objects.filter(codigo_acesso=codigo_acesso).first()
        convidados_do_grupo = Convidado.objects.filter(grupo__codigo_acesso=codigo_acesso)
        ids_confirmados = request.POST.getlist('confirmacao')
        for convidado in convidados_do_grupo:
            if str(convidado.id) in ids_confirmados:
                convidado.status_confirmacao = 'confirmado'
            else:
                convidado.status_confirmacao = 'pendente' # Or 'recusado' if you prefer
            convidado.save()
            
        grupo.status_confirmacao = True
        grupo.save()
        return redirect(f'/{codigo_acesso}/#rsvp-section')
        
    if request.method == 'GET':
        grupo = Grupo.objects.filter(codigo_acesso=codigo_acesso).first()
        request.grupo = grupo
        if grupo.status_confirmacao:
            return render(request, 'core/home.html', {'request': request})
        elif grupo.status_confirmacao is False:
            convidados_do_grupo = Convidado.objects.filter(grupo__codigo_acesso=codigo_acesso)
            request.convidados = convidados_do_grupo
            return render(request, 'core/home.html', {'request': request})