from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):

    def test_create_user_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'sivaperumal644@gmail.com'
        phone_number = '+918903134939'
        password = 'password'
        first_name = 'Siva Perumal'
        user = get_user_model().objects.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            first_name=first_name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email is normalized"""
        email = 'sivaperumal644@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email,
            phone_number="+918903134939",
            password='password',
            first_name='Siva Perumal'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                phone_number='+919442843180',
                password='password',
                first_name='Siva Perumal'
            )

    def test_new_user_invalid_phone(self):
        """Test creating user with no phone raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='sivaperumal644@gmail.com',
                phone_number=None,
                password='password',
                first_name='Siva Perumal'
            )

    def test_new_user_invalid_password(self):
        """Test creating user with no password raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='sivaperumal644@gmail.com',
                phone_number='+919442843180',
                password=None,
                first_name='Siva Perumal'
            )

    def test_new_user_invalid_first_name(self):
        """Test creating user with no first name raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='Sivaperumal644@gmail.com',
                phone_number='+919442843180',
                password='password',
                first_name=None
            )

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'Sivaperumal644@gmail.com',
            'password',
            '+918903134939',
            'Siva Perumal'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)
