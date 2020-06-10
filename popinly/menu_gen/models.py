from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from .modelStyle import MenuType, ColourPalette, ImpactFontPalette, BaseFontPalette


class Menu(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200)
    menu_type = models.CharField(
        max_length=70, choices=MenuType.choices, default=MenuType.Dinner,
    )
    menu_title = models.CharField(
        max_length=200, error_messages={"required": "Menu Title is Required"}
    )
    created_at = models.DateField(default=timezone.now)

    colour_palette = models.CharField(
        max_length=23, choices=ColourPalette.choices, default=ColourPalette.Formal,
    )

    title_font = models.CharField(
        max_length=31,
        choices=ImpactFontPalette.choices,
        default=ImpactFontPalette.Formal,
    )

    base_font = models.CharField(
        max_length=31, choices=BaseFontPalette.choices, default=BaseFontPalette.Formal,
    )

    def __str__(self):
        return self.menu_title


class MenuSection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=200, error_messages={"required": "Menu section name is Required"}
    )
    description = models.CharField(max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(
        error_messages={"required": "Menu section order is Required"}
    )
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class MenuItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=200, error_messages={"required": "Menu item name is Required"}
    )
    description = models.CharField(max_length=200, blank=True, default="")
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        error_messages={"required": "Menu item price is Required"},
    )
    order = models.PositiveIntegerField(
        error_messages={"required": "Menu item order is Required"}
    )
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
