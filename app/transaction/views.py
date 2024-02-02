from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .validators import TransactionValidator
from decimal import Decimal
from django.http import HttpResponse
from datetime import datetime

@login_required
def index(request):
    transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-id')
    context = {
        'transactions': transactions
    }
    return render(request, 'transactions/index.html', context)

def create(request):
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    context = {'categories': categories}

    if request.method == 'POST':
        data = request.POST
        validator = TransactionValidator()
        if not validator.is_valid(request, data):
            return redirect('transactions.create')

        category = Category.objects.get(id=data['category'])
        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=Decimal(data['amount']),
            date=data['date']
        )

        return redirect('transactions.index')


    return render(request, 'transactions/create.html', context)

def edit(request, id):
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    transaction = Transaction.objects.get(id=id)
    context = {
        'categories': categories,
        'transaction': transaction
    }

    if request.method == 'POST':
        data = request.POST
        validator = TransactionValidator()
        if not validator.is_valid(request, data):
            return redirect('transactions.edit', id=id)

        category = Category.objects.get(id=data['category'])
        date = datetime.strptime(data['date'], '%d.%m.%Y')
        transaction.category = category
        transaction.amount = data['amount']
        transaction.date = date
        transaction.save()

        return redirect('transactions.index')

    return render(request, 'transactions/edit.html', context)

def delete(request):
    if request.method == "POST":
        transaction = Transaction.objects.get(id=request.POST['id'])
        transaction.delete()
        return HttpResponse('')