from django.contrib import admin
from .models import Grupo, Convidado

admin.site.site_header = "Administração do Casamento"
admin.site.site_title = "Admin do Casamento"
admin.site.index_title = "Bem-vindo ao Admin do Casamento"


class ConvidadoInline(admin.TabularInline):
    model = Convidado
    fields = ("nome", "status_confirmacao")
    can_delete = False
    extra = 0
    ordering = ("nome",)


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ("nome", "status_confirmacao", "total_convidados", "codigo_acesso")
    list_display_links = ("nome",)
    list_filter = ("status_confirmacao",)
    search_fields = ("nome", "codigo_acesso")
    readonly_fields = ("codigo_acesso",)
    ordering = ("nome",)
    list_per_page = 20
    fieldsets = (
        ("Informações do grupo", {"fields": ("nome", "status_confirmacao", "codigo_acesso")}),
    )
    inlines = [ConvidadoInline]

    def total_convidados(self, obj):
        return obj.convidados.count()

    total_convidados.short_description = "Qtd. Convidados"


@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ("nome", "grupo", "status_confirmacao")
    list_display_links = ("nome",)
    list_filter = ("status_confirmacao", "grupo")
    search_fields = ("nome", "grupo__nome")
    autocomplete_fields = ["grupo"]
    ordering = ("nome",)
    list_per_page = 30
    fieldsets = (
        ("Dados do convidado", {"fields": ("nome", "grupo", "status_confirmacao")}),
    )