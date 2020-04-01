from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu/add/", views.MenuCreateView.as_view(), name="menu_add"),
    path("menu/edit/<menu_id>", views.MenuItemsUpdateView, name="menu_edit"),
]
