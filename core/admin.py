from django.contrib import admin, messages
from django.utils.html import format_html
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
    list_display = (
        "nome",
        "status_confirmacao",
        "total_convidados",
        "codigo_curto",
        "link_encurtado",
        "codigo_acesso",
    )
    list_display_links = ("nome",)
    list_filter = ("status_confirmacao",)
    search_fields = ("nome", "codigo_curto", "codigo_acesso")
    readonly_fields = ("codigo_acesso", "codigo_curto", "link_convite", "link_encurtado")
    ordering = ("nome",)
    list_per_page = 20
    fieldsets = (
        (
            "Informações do grupo",
            {
                "fields": (
                    "nome",
                    "status_confirmacao",
                    "codigo_curto",
                    "link_encurtado",
                    "codigo_acesso",
                    "link_convite",
                )
            },
        ),
    )
    inlines = [ConvidadoInline]
    actions = ["regenerar_codigos_curtos"]

    def total_convidados(self, obj):
        return obj.convidados.count()

    total_convidados.short_description = "Qtd. Convidados"

    @admin.display(description="Link Encurtado")
    def link_encurtado(self, obj):
        if not obj.codigo_curto:
            return "-"
        url = obj.short_url
        return format_html('<a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a>', url)

    @admin.display(description="Link Completo (UUID)")
    def link_convite(self, obj):
        if not obj.pk:
            return "-"
        url = obj.full_url
        return format_html('<a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a>', url)

    @admin.action(description="Regenerar códigos curtos selecionados")
    def regenerar_codigos_curtos(self, request, queryset):
        count = queryset.count()
        for grupo in queryset:
            grupo.codigo_curto = None
            grupo.save()
        self.message_user(
            request, f"{count} código(s) curto(s) regenerado(s) com sucesso."
        )


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