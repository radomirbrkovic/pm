from category.models import Category
from decimal import Decimal
from .models import Fund
from datetime import date, datetime


class FundService:

    def get_list(self, request):
        funds = (Fund.objects.filter(
            user=request.user
        ).order_by('execution_date').
                 prefetch_related('category', 'category__transaction_set'))

        if 'category' in request.GET and int(request.GET['category']) > 0:
            category = Category.objects.get(id=request.GET['category'])
            funds = funds.filter(category=category)

        for fund in funds:
            fund.total_amount = fund.initial_amount

            for transaction in fund.category.transaction_set.all():
                fund.total_amount = fund.total_amount + transaction.amount

        return funds

    def create(self, user, data):
        category = Category.objects.get(id=data['category'])
        Fund.objects.create(
            user=user,
            category=category,
            initial_amount=Decimal(data['initial_amount']),
            target_amount=Decimal(data['target_amount']),
            execution_date=data['execution_date'],
            description=data['description'],
        )

    def update(self, fund, data):
        category = Category.objects.get(id=data['category'])
        date = datetime.strptime(data['execution_date'], '%d.%m.%Y')
        fund.update(category, date, data)

    def delete(self, id):
        fund = Fund.objects.get(id=id)
        fund.delete()

    def show(self, id, request):
        fund = (Fund.objects.
                prefetch_related('category', 'category__transaction_set')
                .get(id=id, user=request.user))
        fund.transactions = fund.category.transaction_set.all()
        fund.total_amount = fund.initial_amount

        for transaction in fund.category.transaction_set.all():
            fund.total_amount = fund.total_amount + transaction.amount

        fund.balance = fund.target_amount - fund.total_amount
        fund.per_month = 0
        if fund.target_amount > fund.total_amount:
            today = date.today()
            months = self._diff_month(fund.execution_date, today) \
                if self._diff_month(fund.execution_date, today) > 0 else 1
            fund.per_month = fund.balance / months

        return fund

    def _diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month
