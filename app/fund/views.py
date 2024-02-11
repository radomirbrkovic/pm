from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from category.models import Category
from .services import FundService
from .models import Fund
from django.http import HttpResponse

service = FundService()

@login_required
def index(request):
    funds = service.getList(request)
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')

    context = {
        'categories': categories,
        'values': request.GET,
        'funds': funds
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

@login_required
def edit(request, id):
    fund = Fund.objects.get(id = id)

    if request.method == 'POST':
        service.update(fund, request.POST)
        return redirect('funds.index')

    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    context = {
        'categories': categories,
        'fund': fund
    }

    return render(request, 'funds/edit.html', context)

@login_required
def delete(request):
    if request.method == "POST":
        service.delete(request.POST['id'])
        return HttpResponse('')