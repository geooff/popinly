from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
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


class MenuListView(ListView):
    model = Menu
    context_object_name = "user_menus"
    template_name = "menu_gen/index.html"

    def get_queryset(self):
        # Add try except to handle non-loggedin users
        queryset = super(MenuListView, self).get_queryset()
        queryset = queryset.filter(author__exact=self.request.user)
        return queryset


class MenuCreateView(CreateView):
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
        return reverse("menu_edit", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "The menu was added.")
        return super().form_valid(form)


class MenuDelete(DeleteView):
    model = Menu
    template_name = "menu_gen/menu_confirm_delete.html"
    context_object_name = "menu"

    def get_success_url(self):
        return reverse("menu_index")

    # TODO: Add logic to make sure only owner of object can delete


class MenuItemsUpdateView(SingleObjectMixin, FormView):
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
        return reverse("menu_edit", kwargs={"pk": self.object.pk})


class MenuDetailView(DetailView):

    model = Menu
    template_name = "menu_gen/menu_detail.html"
    context_object_name = "menu"

    def get_queryset(self):
        # Add try except to handle non-loggedin users
        queryset = super(MenuDetailView, self).get_queryset()
        queryset = queryset.filter(author__exact=self.request.user)
        return queryset
