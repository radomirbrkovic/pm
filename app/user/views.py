from django.shortcuts import render, redirect
from django.contrib import messages, auth

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