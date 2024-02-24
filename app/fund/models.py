from django.db import models
from django.conf import settings
from category.models import Category


class Fund(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    execution_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
