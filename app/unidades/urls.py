from django.urls import path

from .views import UnidadeCreateView, UnidadeDeleteView, UnidadeListView, UnidadeUpdateView

urlpatterns = [
    path("", UnidadeListView.as_view(), name="unidade-list"),
    path("novo/", UnidadeCreateView.as_view(), name="unidade-create"),
    path("<uuid:pk>/editar/", UnidadeUpdateView.as_view(), name="unidade-update"),
    path("<uuid:pk>/excluir/", UnidadeDeleteView.as_view(), name="unidade-delete"),
]
