from django.db import models
from django.utils.translation import gettext_lazy as _


class ColourPalette(models.TextChoices):
    # Follows format Primary Colour, Secondary Colour, Accent Colour
    Formal = "#000000 #000000 #000000", _("Formal")
    Modern = "#702323 #000000 #702323", _("Modern")
    Autumn = "#8f741d #000000 #000000", _("Autumn")
    Fultur = "#1f4027 #0f2113 #1f4037", _("Fultur")
    Oculum = "#266682 #1d2224 #1d2224", _("Oculum")
    Salmon = "#000000 #000000 #c75b5d", _("Salmon")


class ImpactFontPalette(models.TextChoices):
    Formal = "Dancing+Script", _("Danging Script")
    Modern = "Josefin+Sans", _("Josefin Sans")
    Autumn = "Reenie+Beanie", _("Reenie Beanie")
    Fultur = "Nothing+You+Could+Do", _("Nothing You Could Do")
    Oculum = "Tenor+Sans", _("Tenor Sans")


class BaseFontPalette(models.TextChoices):
    Formal = "Roboto", _("Roboto")
    Modern = "Lato", _("Lato")
    Autumn = "Open+Sans", _("Open Sans")
    Fultur = "Montserrat", _("Montserrat")
    Oculum = "Source Sans Pro", _("Source Sans Pro")
