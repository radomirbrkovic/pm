from .models import Category

class CategoryService:
    """List of allowed types"""
    types = (
        ('income_active', "Income - active"),
        ('income_passive', "Income - passive"),
        ('asset', "Asset"),
        ('liability', "Liability"),
    )

    def listOfCategories(self, request):
        categories = Category.objects.filter(
            user=request.user
        )

        if 'type' in request.GET and  request.GET['type'] is not "" :
            categories = categories.filter(type= request.GET['type'])

        return categories.order_by('-id')