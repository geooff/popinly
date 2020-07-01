from django.urls import path

from . import views

app_name = "menu_gen"
urlpatterns = [
    path("", views.MenuListView.as_view(), name="index"),
    path("wizard/", views.MenuWizard.as_view(), name="wizard"),
    path("edit_appearance/<uuid:pk>", views.MenuEditMeta.as_view(), name="edit_meta",),
    path("edit_contents/<uuid:pk>", views.MenuItemsUpdateView.as_view(), name="edit"),
    path("delete/<uuid:pk>", views.MenuDelete.as_view(), name="delete"),
    path("<str:export_format>/<uuid:pk>", views.generate_menu, name="detail"),
]
