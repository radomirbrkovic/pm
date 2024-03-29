from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .service import CategoryService
from .validators import CategoryValidator
from .models import Category
from django.http import HttpResponse

service = CategoryService()


@login_required
def index(request):
    context = {
        'types': service.types,
        'categories': service.list_of_categories(request=request),
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


@login_required
def edit(request, id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        validator = CategoryValidator()

        if not validator.is_valid(request, data):
            return redirect('categories.edit', category.id)

        service.update(category=category, data=data)
        return redirect('categories.index')

    context = {
        'types': service.types,
        'category': category
    }

    return render(request, 'categories/edit.html', context)


@login_required
def delete(request):
    if request.method == "POST":
        service.delete(request.POST['id'])
        return HttpResponse('')
