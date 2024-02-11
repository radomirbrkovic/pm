from category.models import Category
from datetime import datetime
from decimal import Decimal
from .models import Fund

class FundService:

    def getList(self, request):
        funds = Fund.objects.filter(
            user=request.user
        ).order_by('-id')

        if 'category' in request.GET and int(request.GET['category']) > 0:
            category = Category.objects.get(id=request.GET['category'])
            funds = funds.filter(category=category)

        return funds


    def create(self, user, data):
        category = Category.objects.get(id=data['category'])
        Fund.objects.create(
            user = user,
            category = category,
            initial_amount = Decimal(data['initial_amount']),
            target_amount = Decimal(data['target_amount']),
            execution_date = data['execution_date'],
            description = data['description'],
        )