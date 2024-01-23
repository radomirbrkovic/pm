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

    def test_create_user_invalid(self):
        """Test don't create user if email is missing"""
        data = {
            'email': '',
            'name': 'John Doe',
            'password': 'test123'
        }
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                **data
            )

    def test_update_user(self):
        """Testing update a user"""

        data = {
            'email': 'test@example.com',
            'name': 'John Doe',
            'password': 'test123'
        }
        user = get_user_model().objects.create_user(
            **data
        )

        new_name = "New Name"
        user.name = new_name
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.name, new_name)