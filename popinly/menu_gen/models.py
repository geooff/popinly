from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    created_at = models.DateField(default=timezone.now)

    class ColourPalette(models.TextChoices):
        Formal = "#2B2D42 #f0a500 #cf7501 #dbdbdb", _("Formal")
        Modern = "#000000 #8D99AE #D90429 #EF233C", _("Modern")
        Autumn = "#000r00 #f0a502 #cf7503 #dbdbd2", _("Autumn")
        Fultur = "#00e000 #f0a503 #cf7504 #dbdbd3", _("Fultur")
        Oculum = "#000040 #f0a504 #cf7500 #dbdbd4", _("Oculum")

    colour_palette = models.CharField(
        max_length=31, choices=ColourPalette.choices, default=ColourPalette.Formal,
    )

    def __str__(self):
        return self.title


class MenuSection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.item_name


class MenuItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.item_name
