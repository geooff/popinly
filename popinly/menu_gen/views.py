import os

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy


from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import MenuSectionsItemsFormset
from .models import Menu, MenuSection, MenuItem
from .dynamicStyle import userColourTemplate, userFontTemplate

import sass
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
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
        "menu_title",
    ]

    def get_success_url(self):
        return reverse("menu_gen:edit", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MenuCreateView, self).form_valid(form)


class MenuEditMeta(LoginRequiredMixin, UpdateView):
    """
    For editing menu metadata (colour, name, ect..). Adding items to it is done in the
    MenuItemsUpdateView().
    """

    model = Menu
    template_name = "menu_gen/menu_edit_meta.html"
    fields = [
        "restaurant_name",
        "menu_title",
        "colour_palette",
        "title_font",
        "base_font",
    ]

    def get_success_url(self):
        return reverse("menu_gen:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MenuEditMeta, self).form_valid(form)


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
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("menu_gen:edit", kwargs={"pk": self.object.pk})


def generate_menu_pdf(request, pk):
    """Generate pdf."""

    def _generate_colour_palette(menu):
        colours = [x for x in menu.colour_palette.split(" ")]
        body = userColourTemplate()
        return body.format(*colours)

    def _generate_font_palette(menu):
        title = menu.title_font
        base = menu.base_font
        body = userFontTemplate()
        return body.format(
            title_web=title,
            title=title.replace("+", " "),
            base_web=base,
            base=base.replace("+", " "),
        )

    # Model data
    menu = Menu.objects.all().filter(author__exact=request.user).get(pk=pk)

    # Rendered
    html_string = render_to_string("menu_gen/menu_detail.html", {"menu": menu})
    html = HTML(string=html_string)

    # Styling
    font_config = FontConfiguration()
    user_font = _generate_font_palette(menu)
    user_colour = _generate_colour_palette(menu)
    with open(
        os.path.join(os.path.dirname(__file__), "./base_export.scss"), "r"
    ) as template_css_contents:
        template_css = template_css_contents.read()

    css = user_font + user_colour + template_css
    user_css = sass.compile(string=css)
    css_files = [CSS(string=user_css, font_config=font_config)]

    # Generate PDF
    result = html.write_pdf(stylesheets=css_files, font_config=font_config)

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
