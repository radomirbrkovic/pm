from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='funds.index'),
    path('create', views.create, name='funds.create'),
    path('edit/<int:id>', views.edit, name='funds.edit'),
    path('show/<int:id>', views.show, name='funds.show'),
    path('delete', views.delete, name='funds.delete'),
]
