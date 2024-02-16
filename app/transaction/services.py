from .models import  Transaction
from category.models import Category
from datetime import datetime
from decimal import Decimal

class TransactionService:

    def listOfTransactions(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        if 'category' in request.GET and int(request.GET['category']) > 0:
            category = Category.objects.get(id=request.GET['category'])
            transactions = transactions.filter(category=category)

        if 'date' in request.GET:
            date = datetime.strptime(request.GET['date'], '%d.%m.%Y')
            transactions = transactions.filter(date=date)

        return transactions.order_by('-id')

    def create(self, user, data):
        category = Category.objects.get(id=data['category'])
        Transaction.objects.create(
            user=user,
            category=category,
            amount=Decimal(data['amount']),
            date=data['date'],
            description=data['description']
        )

    def update(self, transaction, data):
        category = Category.objects.get(id=data['category'])
        date = datetime.strptime(data['date'], '%d.%m.%Y')
        transaction.category = category
        transaction.amount = data['amount']
        transaction.date = date
        transaction.description = data['description']
        transaction.save()

    def delete(self, id):
        transaction = Transaction.objects.get(id=id)
        transaction.delete()


    def cash_flow(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        data = {}

        for transaction in transactions:
            if transaction.date.strftime("%m%Y") not in data:
                data[transaction.date.strftime("%m%Y")] = {
                    'label': transaction.date.strftime("%B %Y"),
                    'id': transaction.date.strftime("%b-%Y"),
                    'income': 0.0,
                    'expenses': 0.0,
                    'assets': 0.0,
                    'liabilities': 0.0,
                    'assets_share': 0.0,
                    'liabilities_share': 0.0
                }

            if transaction.category.type in ['income_active', 'income_passive']:
                data[transaction.date.strftime("%m%Y")]['income'] = data[transaction.date.strftime("%m%Y")]['income'] + float(transaction.amount)
            else:
                data[transaction.date.strftime("%m%Y")]['expenses'] = data[transaction.date.strftime("%m%Y")][
                                                                        'expenses'] + float(transaction.amount)
                if transaction.category.type == 'asset':
                    data[transaction.date.strftime("%m%Y")]['assets'] = data[transaction.date.strftime("%m%Y")][
                                                                              'assets'] + float(transaction.amount)
                elif transaction.category.type == 'liability':
                    data[transaction.date.strftime("%m%Y")]['liabilities'] = data[transaction.date.strftime("%m%Y")][
                                                                              'liabilities'] + float(transaction.amount)

        for key, item in data.items():
            item['assets_share'] = (item['assets'] / item['income']) * 100
            item['liabilities_share'] = (item['liabilities'] / item['income']) * 100
            item['unallocated'] = item['income'] - item['liabilities']


        return data