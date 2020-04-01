from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
)

from .forms import MenuSectionsItemsFormset
from .models import Menu, MenuSection, MenuItem


def index(request):
    context = {}
    if request.user.is_authenticated:
        user_menus = Menu.objects.filter(author__exact=request.user)
        context = {"user_menus": user_menus}
    return render(request, "menu_gen/index.html", context)


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

    def form_valid(self, form):

        messages.add_message(self.request, messages.SUCCESS, "The menu was added.")

        return super().form_valid(form)


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
        # The Menu we're uploading for:
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
        return reverse("books:publisher_detail", kwargs={"pk": self.object.pk})


# def create_menu(request, menu_id):
#     menu = Menu.objects.get(pk=menu_id)
#     MenuFormset = inlineformset_factory(
#         Menu,
#         MenuItem,
#         fields=["item_name", "item_description", "item_price"],
#         extra=1,
#         can_order=True,
#         can_delete=True,
#         min_num=1,
#     )

#     if request.method == "POST":
#         formset = MenuFormset(request.POST, instance=menu)
#         if formset.is_valid():
#             formset.save()
#             return redirect("create_menu", menu_id=menu.menu_id)

#     formset = MenuFormset(instance=menu)
#     return render(request, "menu_gen/edit_menu.html", {"formset": formset})


# def create_menu(request, menu_id):
#     menu = Menu.objects.get(pk=menu_id)
#     MenuFormset = inlineformset_factory(
#         Menu,
#         MenuItem,
#         fields=["item_name", "item_description", "item_price"],
#         extra=1,
#         can_order=True,
#         can_delete=True,
#         min_num=1,
#     )

#     if request.method == "POST":
#         formset = MenuFormset(request.POST, instance=menu)
#         if formset.is_valid():
#             formset.save()
#             return redirect("create_menu", menu_id=menu.menu_id)

#     formset = MenuFormset(instance=menu)
#     return render(request, "menu_gen/edit_menu.html", {"formset": formset})


# def generate_menu(request):
#     # TODO: call the pdf menu generator here, something like make_latex_menu()
#     # Function should return the directory the file is saved in, file loc will be used in file response
#     return FileResponse(
#         open("myfile.png", "rb"), as_attachment=True, filename="menu.pdf"
#     )
