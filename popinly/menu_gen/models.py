from django.db import models


class Menu(models.Model):
    restaurant = models.CharField(max_length=200)
    menu_body = JSONField()
    pub_date = models.IntegerField(default=0)
