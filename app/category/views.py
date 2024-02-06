from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .service import CategoryService

service = CategoryService()

@login_required
def index(request):
    context = {
        'types': service.types,
        'categories': service.listOfCategories(request=request),
        'values': request.GET
    }

    return render(request, 'categories/index.html', context)