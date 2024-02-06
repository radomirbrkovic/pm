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


    def listOfCategories(self, request):
        categories = Category.objects.filter(
            user=request.user
        )

        if 'type' in request.GET and  request.GET['type'] is not "" :
            categories = categories.filter(type= request.GET['type'])

        categories = categories.order_by('-id').prefetch_related('transaction_set')

        for category in categories:
            category.type_name = self.types[category.type]
            category.total_transaction = Decimal('0')

            for transaction in category.transaction_set.all() :
                category.total_transaction = category.total_transaction + transaction.amount


        return categories