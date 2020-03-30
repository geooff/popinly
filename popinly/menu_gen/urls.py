from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="generator_index"),
    path("create/<menu_id>", views.create_menu, name="create_menu"),
]
