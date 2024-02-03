from .models import  Transaction, Category
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
            date=data['date']
        )

    def update(self, transaction, data):
        category = Category.objects.get(id=data['category'])
        date = datetime.strptime(data['date'], '%d.%m.%Y')
        transaction.category = category
        transaction.amount = data['amount']
        transaction.date = date
        transaction.save()

    def delete(self, id):
        transaction = Transaction.objects.get(id=id)
        transaction.delete()
