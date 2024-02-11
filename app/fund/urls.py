from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='funds.index'),
    path('create', views.create, name='funds.create'),
]