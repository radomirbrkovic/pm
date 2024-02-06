from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='categories.index'),
    #path('create', views.create, name='categories.create'),
    #path('create/<int:id>', views.edit, name='categories.edit'),
]