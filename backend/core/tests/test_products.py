from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Product, User


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="test",
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            password="test",
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=9.99,
            stock=10,
        )
        self.url = reverse("product-detail", kwargs={"product_id": self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_unathorized_update_product(self):
        data = {"name": "Updated Product"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unathorized_delete_product(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product(self):
        # test normal user cannot delete
        self.client.login(email="user@example.com", password="test")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

        # test admin can delete
        self.client.login(email="admin@example.com", password="test")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
