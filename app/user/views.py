from django.shortcuts import render
from django.contrib import messages

def index(request):
    return render(request, 'base.html')

def login(request):
    return  render(request, 'auth/login.html')