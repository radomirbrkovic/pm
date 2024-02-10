from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from category.models import Category

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
    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')
    context = {
        'categories': categories
    }

    return render(request, 'funds/create.html', context)