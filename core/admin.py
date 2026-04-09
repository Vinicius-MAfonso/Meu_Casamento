from django.contrib import admin
from .models import Grupo, Convidado

# Configure admin site
admin.site.site_header = "Administração do Casamento"
admin.site.site_title = "Admin do Casamento"
admin.site.index_title = "Bem-vindo ao Admin do Casamento"

class ConvidadoInline(admin.TabularInline):
    model = Convidado
    extra = 1  
    classes = ('collapse',)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'codigo_acesso', 
        'status_confirmacao', 
        'total_convidados'
    )
    list_filter = ('status_confirmacao',)
    search_fields = ('nome', 'codigo_acesso')
    
    readonly_fields = ('codigo_acesso',)
    
    inlines = [ConvidadoInline]

    def total_convidados(self, obj):
        return obj.convidados.count()
    total_convidados.short_description = "Qtd. Convidados"


@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'grupo', 
        'status_confirmacao'
    )
    list_filter = (
        'status_confirmacao', 
        'grupo'
    )
    search_fields = ('nome', 'grupo__nome')
    
    autocomplete_fields = ['grupo'] 
    
    list_editable = ('status_confirmacao',)