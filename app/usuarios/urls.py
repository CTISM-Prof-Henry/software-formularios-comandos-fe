from django.urls import path

from .views import (
    UsuarioCreateView,
    UsuarioDeleteView,
    UsuarioListView,
    UsuarioResetPasswordView,
    UsuarioUpdateView,
)

urlpatterns = [
    path("", UsuarioListView.as_view(), name="usuario-list"),
    path("novo/", UsuarioCreateView.as_view(), name="usuario-create"),
    path("<uuid:pk>/editar/", UsuarioUpdateView.as_view(), name="usuario-update"),
    path(
        "<uuid:pk>/resetar-senha/",
        UsuarioResetPasswordView.as_view(),
        name="usuario-reset-password",
    ),
    path("<uuid:pk>/excluir/", UsuarioDeleteView.as_view(), name="usuario-delete"),
]
