from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generator/", include("menu_gen.urls")),
    path("admin/", admin.site.urls),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Add Django site authentication urls (for login, logout, password management)
]
