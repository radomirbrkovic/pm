from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category

@login_required
def index(request):
    transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-id')
    context = {
        'transactions': transactions
    }
    return render(request, 'transactions/index.html', context)
