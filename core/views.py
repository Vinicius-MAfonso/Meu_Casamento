from django.shortcuts import render

def home(request, codigo_acesso):
    if request.method == 'POST':
        pass
        
    if request.method == 'GET':
        return render(request, 'home.html', {'codigo_acesso': codigo_acesso})