from category.models import Category
from datetime import datetime
from decimal import Decimal
from .models import Fund
from transaction.models import Transaction
from django.db.models import Sum

class FundService:

    def getList(self, request):
        funds = Fund.objects.filter(
            user=request.user
        ).order_by('execution_date')

        if 'category' in request.GET and int(request.GET['category']) > 0:
            category = Category.objects.get(id=request.GET['category'])
            funds = funds.filter(category=category)

        for fund in funds:
            total_transactions = Transaction.objects.filter(category=fund.category).aggregate(Sum('amount'))
            fund.total_amount = fund.initial_amount

            if total_transactions['amount__sum']:
                fund.total_amount = fund.total_amount + total_transactions['amount__sum']

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

    def update(self, fund, data):
        category = Category.objects.get(id=data['category'])
        date = datetime.strptime(data['execution_date'], '%d.%m.%Y')
        fund.category = category
        fund.execution_date = date
        fund.initial_amount = Decimal(data['initial_amount'])
        fund.target_amount = Decimal(data['target_amount'])
        fund.description = data['description']
        fund.save()

    def delete(self, id):
        fund = Fund.objects.get(id=id)
        fund.delete()


    def show(self, id, request):
        fund = Fund.objects.get(id=id, user=request.user)
        fund.transactions = Transaction.objects.filter(category=fund.category)
        total_transactions = Transaction.objects.filter(category=fund.category).aggregate(Sum('amount'))
        fund.total_amount = fund.initial_amount

        if total_transactions['amount__sum']:
            fund.total_amount = fund.total_amount + total_transactions['amount__sum']



        return fund