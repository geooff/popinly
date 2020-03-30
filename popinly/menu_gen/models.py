import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Menu(models.Model):
    menu_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200)
    menu_title = models.CharField(max_length=200)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.menu_title


class MenuItem(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.item_name
