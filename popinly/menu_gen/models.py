from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


class Menu(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    created_at = models.DateField(default=timezone.now)

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
