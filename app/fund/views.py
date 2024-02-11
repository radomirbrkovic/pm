from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from category.models import Category
from .services import FundService

service = FundService()

@login_required
def index(request):
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')

    context = {
        'categories': categories,
        'values': request.GET
    }

    return render(request, 'funds/index.html', context)

@login_required
def create(request):

    if request.method == 'POST':
        service.create(request.user, request.POST)
        return redirect('funds.index')

    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    context = {
        'categories': categories
    }

    return render(request, 'funds/create.html', context)