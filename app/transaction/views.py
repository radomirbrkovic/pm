from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from category.models import Category
from .validators import TransactionValidator
from django.http import HttpResponse
from .services import TransactionService

service = TransactionService()


@login_required
def index(request):
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    transactions = service.list_of_transactions(request)

    context = {
        'transactions': transactions,
        'categories': categories,
        'values': request.GET
    }
    return render(request, 'transactions/index.html', context)


@login_required
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


@login_required
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


@login_required
def delete(request):
    if request.method == "POST":
        service.delete(request.POST['id'])
        return HttpResponse('')


@login_required
def cash_flow(request):
    data = service.cash_flow(request)
    context = {
        'data': data
    }
    return render(request, 'transactions/cash-flow.html', context)


@login_required
def dashboard(request):
    data = service.dashboard(request)
    context = {
        'data': data
    }
    return render(request, 'transactions/dashboard.html', context)
