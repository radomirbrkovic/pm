from django.contrib import messages
from .service import CategoryService
from .models import Category

class CategoryValidator:

    def is_valid(self, request, data) -> bool:
        service = CategoryService()
        if data['type'] not in service.types:
            messages.error(request, "The category type is invalid")
            return False

        if Category.objects.filter(name=data['name'], type=data['type']).exists():
            messages.error(request, "The category already exists")
            return False

        return True