from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import User
from .validators import Register

def index(request):
    return render(request, 'base.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Ypu are now login")
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return  render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        validator = Register()
        if not validator.is_valid(request, data):
            return redirect('register')

        user = User.objects.create_user(email=data['email'], name=data['name'], password=data['password'])
        user.save()

        messages.success(request, "You are successfully create account.")
        return redirect('login')

    return render(request, 'auth/register.html')