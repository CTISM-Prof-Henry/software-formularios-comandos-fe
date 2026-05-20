from django.contrib import admin

from .models import Unidade


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome", "tipo_unidade", "unidade_pai")
    list_filter = ("tipo_unidade",)
    search_fields = ("sigla", "nome")
