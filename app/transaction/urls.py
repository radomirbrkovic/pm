from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='transactions.index'),
    path('create', views.create, name='transactions.create'),
    path('edit/<int:id>', views.edit, name='transactions.edit'),
    path('delete', views.delete, name='transactions.delete'),
]