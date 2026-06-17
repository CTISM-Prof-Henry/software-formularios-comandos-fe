from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class PageContextMixin:
    page_title = ""
    page_description = ""

    def get_page_title(self):
        return self.page_title

    def get_page_description(self):
        return self.page_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("page_title", self.get_page_title())
        context.setdefault("page_description", self.get_page_description())
        return context


class CrudListView(PageContextMixin, ListView):
    template_name = "crud/list.html"
    context_object_name = "objects"
    create_url_name = None
    update_url_name = None
    delete_url_name = None
    create_label = "Novo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = (
            reverse_lazy(self.create_url_name) if self.create_url_name else None
        )
        context["update_name"] = self.update_url_name
        context["delete_name"] = self.delete_url_name
        context["create_label"] = self.create_label
        context["list_model_name"] = self.model._meta.model_name
        return context


class CrudFormView(PageContextMixin):
    template_name = "crud/form.html"
    cancel_url_name = None
    submit_label = "Salvar"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = (
            reverse_lazy(self.cancel_url_name) if self.cancel_url_name else None
        )
        context["submit_label"] = self.submit_label
        return context


class CrudCreateView(CrudFormView, CreateView):
    pass


class CrudUpdateView(CrudFormView, UpdateView):
    pass


class CrudDeleteView(PageContextMixin, DeleteView):
    template_name = "crud/confirm_delete.html"
    cancel_url_name = None
    delete_label = "Excluir"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = (
            reverse_lazy(self.cancel_url_name) if self.cancel_url_name else None
        )
        context["delete_label"] = self.delete_label
        return context
