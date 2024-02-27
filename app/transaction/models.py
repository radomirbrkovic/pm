from django.db import models
from django.conf import settings
from category.models import Category


class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def update(self, category, amount, date, description):
        self.category = category
        self.amount = amount
        self.date = date
        self.description = description
        self.save()