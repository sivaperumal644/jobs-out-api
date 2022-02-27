from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

LOGIN_URL = reverse("user:login")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class LoginUserAPITests(TestCase):
    """Test the login API"""

    def setUp(self):
        self.client = APIClient()

        payload = {
            "email": "tester@gmail.com",
            "password": "password",
            "phone_number": "+917339195584",
            "first_name": "Siva Perumal",
        }

        create_user(**payload)

    def test_login_successful(self):
        """Test login successful with correct credentials"""
        payload = {"email": "tester@gmail.com", "password": "password"}

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_failed(self):
        """Test login fails with invalid credentials"""

        payload = {"email": "tester@gmail.com", "password": "password123"}

        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_not_exist(self):
        """Test login fails if user does not exist"""
        payload = {"email": "test@gmail.com", "password": "password"}

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_email_required(self):
        """Test login fails when email is not given"""

        payload = {"email": None, "password": "password"}

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_password_required(self):
        """Test login fails when password is not given"""

        payload = {"email": "tester@gmail.com", "password": None}

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
