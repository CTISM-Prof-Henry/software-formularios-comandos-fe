from django.urls import path

from .views import (
    RiscoCreateView,
    RiscoDeleteView,
    RiscoListView,
    RiscoPrintView,
    RiscoUpdateView,
)

urlpatterns = [
    path("", RiscoListView.as_view(), name="risco-list"),
    path("novo/", RiscoCreateView.as_view(), name="risco-create"),
    path("<uuid:pk>/editar/", RiscoUpdateView.as_view(), name="risco-update"),
    path("<uuid:pk>/excluir/", RiscoDeleteView.as_view(), name="risco-delete"),
    path("<uuid:pk>/imprimir/", RiscoPrintView.as_view(), name="risco-print"),
]
