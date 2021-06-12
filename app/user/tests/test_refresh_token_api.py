from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# REFRESH_TOKEN_URL = reverse('user:refresh_token')
# LOGIN_URL = reverse('user:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class RefreshTokenAPITests(TestCase):
    """Test the Refresh Token API"""

    def setUp(self):
        self.client = APIClient()

        payload = {
            'email': 'tester@gmail.com',
            'password': 'password',
            'phone_number': '+917339195584',
            'first_name': 'Siva Perumal'
        }

        res = self.client.post(
            LOGIN_URL, {'email': 'tester@gmail.com', 'password': 'password'})
        self.token = res['token']
        self.invalid_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoic2l2YXBlcnVtYWxAZ21haWwuY29tIiwiZXhwIjoxNjI4NjA2Mzk5LCJpYXQiOjE2MjM0MjIzOTl9.8nbgqXfEZ8yhYjFwaL47v7dOwi_Bfvgvu4S1Ttw6kO8'
        self.expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidGVzdGVyQGdtYWlsLmNvbSIsImV4cCI6MTYyMzQyMjA4NSwiaWF0IjoxNjIzNDIxNzg1fQ.TuTCYfeS2H7RctVPCF3wZ3kypb2ZkDx4SEA0NzJFTb8'

    # def test_refresh_token_successful(self):
    #     """Test whether refresh token API succeeds with proper token"""

    #     res = self.client.post(
    #         REFRESH_TOKEN_URL,
    #         {'refresh_token': self.token['refresh_token']}
    #     )

    #     self.assertTrue(res.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', res.data)

    # def test_refresh_token_invalid(self):
    #     """Test whether refresh token API fails with invalid refresh token"""

    #     res = self.client.post(
    #         REFRESH_TOKEN_URL,
    #         {'refresh_token': self.invalid_token}
    #     )

    #     self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_refresh_token_expired(self):
    #     """Test whether refresh token API fails with expired refresh token"""

    #     res = self.client.post(
    #         REFRESH_TOKEN_URL,
    #         {'refresh_token': self.expired_token}
    #     )

    #     self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_refresh_token_required(self):
    #     """Test whether API fails when refresh token is not passed"""

    #     res = self.client.post(
    #         REFRESH_TOKEN_URL,
    #         {'refresh_token': None}
    #     )

    #     self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)
