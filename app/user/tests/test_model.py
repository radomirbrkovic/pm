"""
Test user model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        user = get_user_model().objects.create_user(
            email="test@email.com",
            password="test123"
        )

        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.check_password("test123"))
