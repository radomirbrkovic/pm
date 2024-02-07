from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .service import CategoryService
from .validators import CategoryValidator

service = CategoryService()

@login_required
def index(request):
    context = {
        'types': service.types,
        'categories': service.listOfCategories(request=request),
        'values': request.GET
    }

    return render(request, 'categories/index.html', context)

@login_required
def create(request):

    if request.method == 'POST':
        data = request.POST
        validator = CategoryValidator()

        if not validator.is_valid(request, data):
            return redirect('categories.create')

        service.create(user=request.user, data=data)
        return redirect('categories.index')


    context = {
        'types': service.types
    }

    return render(request, 'categories/create.html', context)