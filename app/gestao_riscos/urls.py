from django.contrib import admin
from django.urls import include, path

from .views import healthcheck, index


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("usuarios/", include("usuarios.urls")),
    path("unidades/", include("unidades.urls")),
]
