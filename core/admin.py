import logging
from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Grupo, Convidado
from .utils import shorten_url_tinyurl

logger = logging.getLogger(__name__)

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
        "codigo_acesso",
        "link_convite",
        "link_encurtado",
    )
    list_display_links = ("nome",)
    list_filter = ("status_confirmacao",)
    search_fields = ("nome", "codigo_acesso")
    readonly_fields = ("codigo_acesso", "link_convite", "link_encurtado")
    ordering = ("nome",)
    list_per_page = 20
    fieldsets = (
        (
            "Informações do grupo",
            {
                "fields": (
                    "nome",
                    "status_confirmacao",
                    "codigo_acesso",
                    "link_convite",
                    "encurtador_url",
                    "link_encurtado",
                )
            },
        ),
    )
    inlines = [ConvidadoInline]
    actions = ["gerar_links_encurtados"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.encurtador_url:
            try:
                obj.encurtador_url = shorten_url_tinyurl(obj.full_url)
                obj.save(update_fields=["encurtador_url"])
            except Exception as e:
                logger.warning("Falha ao gerar link encurtado para %s: %s", obj, e)

    def total_convidados(self, obj):
        return obj.convidados.count()

    total_convidados.short_description = "Qtd. Convidados"

    @admin.display(description="Link do Convite")
    def link_convite(self, obj):
        if not obj.pk:
            return "-"
        url = obj.full_url
        return format_html('<a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a>', url)

    @admin.display(description="Link Encurtado")
    def link_encurtado(self, obj):
        if obj.encurtador_url:
            return format_html(
                '<a href="{0}" target="_blank" rel="noopener noreferrer">{0}</a>',
                obj.encurtador_url,
            )
        return "-"

    @admin.action(description="Gerar link encurtado via TinyURL")
    def gerar_links_encurtados(self, request, queryset):
        grupos_para_gerar = [g for g in queryset if not g.encurtador_url]
        # If all selected groups already have a link, allow re-generating for them
        if not grupos_para_gerar and queryset.exists():
            grupos_para_gerar = list(queryset)

        success_count = 0
        error_count = 0
        for grupo in grupos_para_gerar:
            try:
                grupo.encurtador_url = shorten_url_tinyurl(grupo.full_url)
                grupo.save(update_fields=["encurtador_url"])
                success_count += 1
            except Exception as e:
                logger.warning("Falha ao gerar link encurtado para %s: %s", grupo, e)
                error_count += 1

        already_had = queryset.count() - len(grupos_para_gerar)

        if success_count:
            msg = f"{success_count} link(s) encurtado(s) gerado(s) com sucesso."
            if already_had > 0:
                msg += f" ({already_had} grupo(s) já possuíam link e foram mantidos)."
            self.message_user(request, msg)
        if error_count:
            self.message_user(
                request,
                f"Falha ao gerar link encurtado para {error_count} grupo(s).",
                level=messages.WARNING,
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