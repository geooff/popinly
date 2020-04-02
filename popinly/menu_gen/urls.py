from django.urls import path

from . import views

urlpatterns = [
    path("", views.MenuListView.as_view(), name="menu_index"),
    path("add/", views.MenuCreateView.as_view(), name="menu_add"),
    path("edit/<uuid:pk>", views.MenuItemsUpdateView.as_view(), name="menu_edit"),
]
