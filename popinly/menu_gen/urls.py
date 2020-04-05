from django.urls import path

from . import views

app_name = "menu_gen"
urlpatterns = [
    path("", views.MenuListView.as_view(), name="index"),
    path("add/", views.MenuCreateView.as_view(), name="add"),
    path("edit/<uuid:pk>", views.MenuItemsUpdateView.as_view(), name="edit"),
    path("delete/<uuid:pk>", views.MenuDelete.as_view(), name="delete"),
    path("<uuid:pk>", views.MenuDetailView.as_view(), name="detail"),
]
