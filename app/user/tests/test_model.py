"""
Test user model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        data = {
            'email': 'test@example.com',
            'name': 'John Doe',
            'password': 'test123'
        }
        user = get_user_model().objects.create_user(
            **data
        )

        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertTrue(user.check_password(data['password']))
