from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("features/", views.features, name="features"),
    path("generator/", include("menu_gen.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.RegisterView.as_view(), name="register"),
]
