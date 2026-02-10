from django.contrib import admin
from .models import Grupo, Convidado

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
        'is_representante', 
        'status_confirmacao'
    )
    list_filter = (
        'status_confirmacao', 
        'is_representante', 
        'grupo'
    )
    search_fields = ('nome', 'grupo__nome')
    
    autocomplete_fields = ['grupo'] 
    
    list_editable = ('status_confirmacao',)