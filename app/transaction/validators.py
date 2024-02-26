"""
Custom form validators to handle form request
"""
from category.models import Category
from django.contrib import messages


class TransactionValidator:

    def is_valid(self, request, data) -> bool:

        if float(data['amount']) <= 0:
            messages.error(request, "Amount must be greater than zero.")
            return False

        if not Category.objects.filter(id=data['category']).exists():
            messages.error(request, "Invalid category")
            return False

        return True
