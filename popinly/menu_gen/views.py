from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
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

from weasyprint import HTML, CSS
from django.template.loader import render_to_string
import tempfile


class MenuListView(LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = "user_menus"
    template_name = "menu_gen/index.html"

    # Make sure object can only be viewed by object owner
    def get_queryset(self):
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
        "restaurant_name",
        "title",
    ]

    def get_success_url(self):
        return reverse("menu_gen:edit", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "The menu was added.")
        form.instance.author = self.request.user
        return super(MenuCreateView, self).form_valid(form)


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


def generate_menu_pdf(request, pk):
    """Generate pdf."""
    # Model data
    menu = Menu.objects.all().filter(author__exact=request.user).get(pk=pk)

    # Rendered
    html_string = render_to_string("menu_gen/menu_detail.html", {"menu": menu})
    html = HTML(string=html_string)

    # Styling
    css_files = [CSS("static/base_export.css"), CSS("static/bootstrap.min.css")]

    # Generate PDF
    result = html.write_pdf(stylesheets=css_files)

    # Creating http response
    response = HttpResponse(content_type="application/pdf;")
    response["Content-Disposition"] = "inline; filename=menu.pdf"
    response["Content-Transfer-Encoding"] = "binary"
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
