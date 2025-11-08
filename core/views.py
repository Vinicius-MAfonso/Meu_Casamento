from django.shortcuts import render
from .models import Convidado, Grupo

def home(request, codigo_acesso):
    if request.method == 'POST':
        pass
        
    if request.method == 'GET':
        convidados_do_grupo = Convidado.objects.filter(grupo__codigo_acesso=codigo_acesso)
        grupo = Grupo.objects.filter(codigo_acesso=codigo_acesso).first()
        request.convidados = convidados_do_grupo
        request.grupo = grupo
        return render(request, 'core/home.html', {'codigo_acesso': codigo_acesso, 'request': request})