from django.contrib import admin

from .models import Desafio, Macroprocesso, Objetivo, Risco


class ObjetivoInline(admin.TabularInline):
    model = Objetivo
    extra = 0


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome")
    search_fields = ("codigo", "nome")
    inlines = [ObjetivoInline]


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "desafio", "descricao")
    list_filter = ("desafio",)
    search_fields = ("codigo", "descricao")


@admin.register(Macroprocesso)
class MacroprocessoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Risco)
class RiscoAdmin(admin.ModelAdmin):
    list_display = (
        "unidade",
        "tipo_risco",
        "desafio",
        "objetivo",
        "macroprocesso",
        "probabilidade",
        "impacto",
        "nivel_risco",
        "nivel_residual",
        "situacao",
        "criado_por_nome",
        "criado_por_unidade",
    )
    list_filter = (
        "tipo_risco",
        "desafio",
        "macroprocesso",
        "situacao",
        "resposta",
        "criado_por_unidade",
    )
    search_fields = (
        "unidade__sigla",
        "unidade__nome",
        "objetivo__codigo",
        "objetivo__descricao",
        "macroprocesso__nome",
        "risco_identificado",
    )
