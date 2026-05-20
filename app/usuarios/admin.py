from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "email", "perfil_acesso", "unidade")
    list_filter = ("perfil_acesso", "unidade")
    search_fields = ("nome", "matricula", "email")
