from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Order, User


class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="test"
        )
        user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="test"
        )
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user2")
        self.client.force_login(user)
        response = self.client.get(reverse("order-list"))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
