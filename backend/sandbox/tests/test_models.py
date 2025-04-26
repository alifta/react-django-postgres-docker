
from django.contrib.auth import get_user_model
from django.test import TestCase


# A helper function to create a test user
def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test sandbox models."""

    def test_create_user_with_email_successful(self):
        """Test creating a new restaurant"""
        # add some code here

        # self.assertEqual(user.email, email)
        # self.assertTrue(user.check_password(password))
        pass
