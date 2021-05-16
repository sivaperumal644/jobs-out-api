from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_URL = reverse('user:register')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class RegisterUserApiTests(TestCase):
    "Test the register API"

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        "Test creating a user with valid payload"
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'Tester',
            'phone_number': '+917324567890'
        }

        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data['user'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test user already exists with this email"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'Tester',
            'phone_number': '+917324567890'
        }
        create_user(**payload)

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is not less than 8 characters"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'passwor',
            'first_name': 'Tester',
            'phone_number': '+917324567890'
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_email_required(self):
        """Test that register API fails without email"""
        payload = {
            'email': None,
            'password': 'password',
            'first_name': 'Tester',
            'phone_number': '+917324567890'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_required(self):
        """Test that register API fails without password"""
        payload = {
            'email': 'tester@gmail.com',
            'password': None,
            'first_name': 'Tester',
            'phone_number': '+917324567890'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_first_name_required(self):
        """Test that register API fails without first name"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': None,
            'phone_number': '+917324567890'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_number_required(self):
        """Test that register API fails without phone number"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'Tester',
            'phone_number': None
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_payload(self):
        payload = {}

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_gender_choices(self):
        """Test Create User with valid gender is successful"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'siva',
            'phone_number': '+917324567890',
            'gender': 'M'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_invalid_gender_choices(self):
        """Test Create User with invalid gender fails"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'siva',
            'phone_number': '+917324567890',
            'gender': 'male'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_format(self):
        """Test invalid email format is validated"""
        payload = {
            'email': 'tester',
            'password': 'password',
            'first_name': 'siva',
            'phone_number': '+917324567890',
            'gender': 'male'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone_number(self):
        """Test invalid phone number format is validated"""
        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'first_name': 'siva',
            'phone_number': '7324567890',
            'gender': 'male'
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
