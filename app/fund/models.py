from django.db import models
from django.conf import settings
from category.models import Category
from decimal import Decimal


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

    def update(self, category, date, data):
        self.category = category
        self.execution_date = date
        self.initial_amount = Decimal(data['initial_amount'])
        self.target_amount = Decimal(data['target_amount'])
        self.description = data['description']
        self.save()
