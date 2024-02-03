from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .validators import TransactionValidator
from django.http import HttpResponse
from .services import TransactionService

service = TransactionService()

@login_required
def index(request):
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    transactions = service.listOfTransactions(request)

    context = {
        'transactions': transactions,
        'categories': categories,
        'values': request.GET
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
        service.create(request.user, data)
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
        service.update(transaction, data)
        return redirect('transactions.index')

    return render(request, 'transactions/edit.html', context)

def delete(request):
    if request.method == "POST":
        service.delete(request.POST['id'])
        return HttpResponse('')