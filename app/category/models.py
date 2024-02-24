from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=(
        ('income_active', "Income - active"),
        ('income_passive', "Income - passive"),
        ('asset', "Asset"),
        ('liability', "Liability"),
    ), default='income_active')

    def __str__(self):
        return self.name
