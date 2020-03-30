# from django.http import FileResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Menu, MenuItem
from django.forms import inlineformset_factory


def index(request):
    user_menus = Menu.objects.filter(author__exact=request.user)
    return render(request, "menu_gen/index.html", {"user_menus": user_menus})


def create_menu(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    MenuFormset = inlineformset_factory(
        Menu,
        MenuItem,
        fields=["item_name", "item_description", "item_price"],
        extra=0,
        can_order=True,
        can_delete=True,
        min_num=1,
    )

    if request.method == "POST":
        formset = MenuFormset(request.POST, instance=menu)
        if formset.is_valid():
            formset.save()
            return redirect("create_menu", menu_id=menu.menu_id)

    formset = MenuFormset(instance=menu)
    return render(request, "menu_gen/edit_menu.html", {"formset": formset})


# def generate_menu(request):
#     # TODO: call the pdf menu generator here, something like make_latex_menu()
#     # Function should return the directory the file is saved in, file loc will be used in file response
#     return FileResponse(
#         open("myfile.png", "rb"), as_attachment=True, filename="menu.pdf"
#     )
