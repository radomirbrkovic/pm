"""
Custom form validators to handle form request
"""
from django.contrib import messages
from .models import User


class Register:

    def is_valid(self, request, data) -> bool:
        if (data['password'] != data['password2']):
            messages.error(request, 'Password is not equal')
            return False

        if User.objects.filter(email=data['email']).exists():
            messages.error(request, 'The email is already taken')
            return False

        return True
