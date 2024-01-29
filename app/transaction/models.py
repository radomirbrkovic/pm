from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=(
        ('revenue', "Revenue"),
        ('asset', "Asset"),
        ('liability', "Liability"),
    ), default='revenue')

    def __str__(self):
        return self.name