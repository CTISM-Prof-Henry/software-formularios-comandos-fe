from django.contrib import admin
from django.urls import include, path

from .views import (
    app_logout,
    atualizar_cadastro,
    healthcheck,
    index,
    login_page,
    local_registration,
    sem_permissao,
)


urlpatterns = [
    path("", index, name="index"),
    path("login/", login_page, name="login"),
    path("cadastro-local/", local_registration, name="local-registration"),
    path("atualizar-cadastro/", atualizar_cadastro, name="atualizar-cadastro"),
    path("sem-permissao/", sem_permissao, name="sem-permissao"),
    path("logout/", app_logout, name="logout"),
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("usuarios/", include("usuarios.urls")),
    path("unidades/", include("unidades.urls")),
    path("riscos/", include("riscos.urls")),
]
