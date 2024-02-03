from .models import  Transaction, Category
from datetime import datetime
from decimal import Decimal

class TransactionService:

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
