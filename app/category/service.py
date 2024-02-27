from .models import Category
from decimal import Decimal


class CategoryService:
    """List of allowed types"""
    types = {
        'income_active':  "Income - active",
        'income_passive': "Income - passive",
        'asset': "Asset",
        'liability': "Liability",
    }

    def list_of_categories(self, request):
        categories = Category.objects.filter(
            user=request.user
        )

        if 'type' in request.GET and request.GET['type'] != "":
            categories = categories.filter(type=request.GET['type'])

        categories = (categories.order_by('-id')
                      .prefetch_related('transaction_set'))

        for category in categories:
            category.type_name = self.types[category.type]
            category.total_transaction = Decimal('0')

            for transaction in category.transaction_set.all():
                category.total_transaction = (
                        category.total_transaction + transaction.amount)

        return categories

    def create(self, user, data):
        Category.objects.create(
            user=user,
            type=data['type'],
            name=data['name'])

    def update(self, category, data):
        category.update(type=data['type'], name=data['name'])

    def delete(self, id):
        category = Category.objects.get(id=id)
        category.delete()
