from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from .sitemap import ViewSitemap
from . import views

sitemaps = {
    "static": ViewSitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("generator/", include("menu_gen.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", views.RegisterView.as_view(), name="register"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
