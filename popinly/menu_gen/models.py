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
    title = models.CharField(
        max_length=200, error_messages={"required": "Menu Title is Required"}
    )
    created_at = models.DateField(default=timezone.now)

    # TODO: Refactor this out to an external file
    class ColourPalette(models.TextChoices):
        Formal = "#000000 #000000 #000000", _("Formal")
        Modern = "#702323 #000000 #702323", _("Modern")
        Autumn = "#000r00 #f0a502 #cf7503", _("Autumn")
        Fultur = "#1f4027 #0f2113 #1f4037", _("Fultur")
        Oculum = "#266682 #1d2224 #1d2224", _("Oculum")

    colour_palette = models.CharField(
        max_length=23, choices=ColourPalette.choices, default=ColourPalette.Formal,
    )

    # TODO: Refactor this out to an external file
    class ImpactFontPalette(models.TextChoices):
        Formal = "Dancing+Script", _("Danging Script")
        Modern = "Josefin+Sans", _("Josefin Sans")
        Autumn = "Reenie+Beanie", _("Reenie Beanie")
        Fultur = "Nothing+You+Could+Do", _("Nothing You Could Do")
        Oculum = "Tenor+Sans", _("Tenor Sans")

    impact_font = models.CharField(
        max_length=31,
        choices=ImpactFontPalette.choices,
        default=ImpactFontPalette.Formal,
    )

    # TODO: Refactor this out to an external file
    class BaseFontPalette(models.TextChoices):
        Formal = "Roboto", _("Roboto")
        Modern = "Lato", _("Lato")
        Autumn = "Open+Sans", _("Open Sans")
        Fultur = "Montserrat", _("Montserrat")
        Oculum = "Source Sans Pro", _("Source Sans Pro")

    base_font = models.CharField(
        max_length=31, choices=BaseFontPalette.choices, default=BaseFontPalette.Formal,
    )

    def __str__(self):
        return self.title


class MenuSection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=200, error_messages={"required": "Menu section name is Required"}
    )
    description = models.CharField(
        max_length=200,
        error_messages={"required": "Menu section description is Required"},
    )
    order = models.IntegerField(
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
    description = models.CharField(
        max_length=200, error_messages={"required": "Menu item description is Required"}
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        error_messages={"required": "Menu item price is Required"},
    )
    order = models.IntegerField(
        error_messages={"required": "Menu item order is Required"}
    )
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
