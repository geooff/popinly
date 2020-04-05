from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    DeleteView,
)

from .forms import MenuSectionsItemsFormset
from .models import Menu, MenuSection, MenuItem

from django_weasyprint import WeasyTemplateResponseMixin


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = "user_menus"
    template_name = "menu_gen/index.html"

    def get_queryset(self):
        # Add try except to handle non-loggedin users
        queryset = super(MenuListView, self).get_queryset()
        queryset = queryset.filter(author__exact=self.request.user)
        return queryset


class MenuCreateView(LoginRequiredMixin, CreateView):
    """
    Only for creating a new menu. Adding items to it is done in the
    MenuItemsUpdateView().
    """

    model = Menu
    template_name = "menu_gen/menu_add.html"
    fields = [
        "author",
        "restaurant_name",
        "title",
    ]

    # TODO: Extend view to use current user as author and restaurant_name as dropdown of resturaunts

    def get_success_url(self):
        return reverse("menu_gen:edit", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "The menu was added.")
        return super().form_valid(form)


class MenuDelete(LoginRequiredMixin, DeleteView):
    model = Menu
    template_name = "menu_gen/menu_confirm_delete.html"
    context_object_name = "menu"

    def get_success_url(self):
        return reverse("menu_gen:index")

    # TODO: Add logic to make sure only owner of object can delete


class MenuItemsUpdateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    For adding sections to a menu, or editing them.
    """

    model = Menu
    template_name = "menu_gen/menu_edit.html"

    def get(self, request, *args, **kwargs):
        # The Menu we're editing:
        self.object = self.get_object(queryset=Menu.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # The Menu we're adding items for:
        self.object = self.get_object(queryset=Menu.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Use our big formset of formsets, and pass in the Menu object.
        """
        return MenuSectionsItemsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        messages.add_message(self.request, messages.SUCCESS, "Changes were saved.")

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("menu_gen:edit", kwargs={"pk": self.object.pk})


class MenuDetailView(LoginRequiredMixin, DetailView):

    model = Menu
    template_name = "menu_gen/menu_detail.html"
    context_object_name = "menu"

    # TODO: Add support for promatically passing in css files for preview

    def get_queryset(self):
        queryset = super(MenuDetailView, self).get_queryset()
        queryset = queryset.filter(author__exact=self.request.user)
        return queryset


class MenuPDFView(WeasyTemplateResponseMixin, MenuDetailView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # pdf_stylesheets = [
    #     settings.STATIC_ROOT + 'css/app.css',
    # ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # suggested filename (is required for attachment!)
    pdf_filename = "menu.pdf"
    export_template = "base_export.html"

    def get_context_data(self, **kwargs):
        context = super(MenuPDFView, self).get_context_data(**kwargs)
        context.update({"override_base": self.export_template})
        return context
