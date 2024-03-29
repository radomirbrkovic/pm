from .models import Transaction
from category.models import Category
from fund.models import Fund
from datetime import datetime
from decimal import Decimal


class TransactionService:

    def list_of_transactions(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        ).prefetch_related('category')

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
        transaction.update(
            category=category,
            date=date,
            amount=data['amount'],
            description=data['description'])

    def delete(self, id):
        transaction = Transaction.objects.get(id=id)
        transaction.delete()

    def cash_flow(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        ).prefetch_related('category')

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

            if (transaction.category.type in
                    ['income_active', 'income_passive']):
                data[transaction.date.strftime("%m%Y")]['income'] =\
                    (data[transaction.date.strftime("%m%Y")]['income'] +
                     float(transaction.amount))
            else:
                data[transaction.date.strftime("%m%Y")]['expenses'] = (
                        data[transaction.date.strftime("%m%Y")]['expenses'] +
                        float(transaction.amount))
                if transaction.category.type == 'asset':
                    data[transaction.date.strftime("%m%Y")]['assets'] = (
                            data[transaction.date.strftime("%m%Y")]['assets'] +
                            float(transaction.amount))
                elif transaction.category.type == 'liability':
                    data[transaction.date.strftime("%m%Y")]['liabilities'] = (
                            data[transaction.date.strftime("%m%Y")]
                            ['liabilities'] +
                            float(transaction.amount))

        for key, item in data.items():
            item['assets_share'] = (item['assets'] / item['income']) * 100
            item['liabilities_share'] = (
                    (item['liabilities'] / item['income']) * 100)
            item['unallocated'] = item['income'] - item['liabilities']

        return data

    def dashboard(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        ).prefetch_related('category')

        funds = (Fund.objects.filter(
            user=request.user
        ).order_by('execution_date').
                 prefetch_related('category'))

        data = {
            'income': 0.0,
            'expenses': 0.0,
            'assets': 0.0,
            'liabilities': 0.0,
            'assets_share': 0.0,
            'liabilities_share': 0.0,
            'net_value': 0.0,
            'total_liabilities': 0.0,
            'chart': {
                'labels': [],
                'assets': {},
                'liabilities': {}
            }
               }
        for fund in funds:
            if fund.category.type == 'asset':
                data['net_value'] = (data['net_value']
                                     + float(fund.initial_amount))
            elif fund.category.type == 'liability':
                data['total_liabilities'] = (data['total_liabilities']
                                             + float(fund.initial_amount))

        for transaction in transactions:
            if (transaction.category.type in
                    ['income_active', 'income_passive']):
                data['income'] =\
                    (data['income'] +
                     float(transaction.amount))
            else:
                data['expenses'] = (data['expenses']
                                    + float(transaction.amount))
                if (transaction.date.strftime("%m-%Y")
                        not in data['chart']['labels']):
                    (data['chart']['labels']
                     .append(transaction.date.strftime("%m-%Y")))

                if transaction.category.type == 'asset':
                    data['assets'] = (data['assets']
                                      + float(transaction.amount))
                    if (transaction.date.strftime("%m-%Y")
                            not in data['chart']['assets']):
                        (data['chart']['assets']
                            [transaction.date.strftime("%m-%Y")]) = (
                                data['net_value'] + float(transaction.amount))
                    else:
                        (data['chart']['assets']
                            [transaction.date.strftime("%m-%Y")]) = (
                            (data['chart']['assets']
                                [transaction.date.strftime("%m-%Y")]) +
                                float(transaction.amount))

                elif transaction.category.type == 'liability':
                    data['liabilities'] = (data['liabilities']
                                           + float(transaction.amount))

                    if (transaction.date.strftime("%m-%Y")
                            not in data['chart']['liabilities']):
                        (data['chart']['liabilities']
                            [transaction.date.strftime("%m-%Y")]) = (
                                data['total_liabilities']
                                + float(transaction.amount))
                    else:
                        (data['chart']['liabilities']
                            [transaction.date.strftime("%m-%Y")]) = (
                                (data['chart']['liabilities']
                                    [transaction.date.strftime("%m-%Y")]) +
                                float(transaction.amount))

        data['unallocated'] = data['income'] - data['liabilities']

        data['assets_share'] = (data['assets'] / data['income']) * 100
        data['liabilities_share'] = (data['liabilities']
                                     / data['income']) * 100

        data['net_value'] = data['net_value'] + data['assets']
        data['total_liabilities'] = (data['total_liabilities']
                                     + data['liabilities'])

        return data
