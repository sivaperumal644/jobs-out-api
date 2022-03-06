from venv import create

from django.test import TestCase
from django.urls import reverse
from general import models
from rest_framework import status
from rest_framework.test import APIClient

STATE_URL = reverse("general:states")


def create_state(**params):
    return models.State.objects.create(**params)


class StateAPITests(TestCase):
    """Test the state API"""

    def setUp(self):
        self.client = APIClient()

        state_one = {"state_name": "Tamil Nadu"}
        state_two = {"state_name": "Kerala"}

        create_state(**state_one)
        create_state(**state_two)
        return super().setUp()

    def test_get_all_states(self):
        """Tests get all states API"""
        res = self.client.get(STATE_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data["states"]), 2)
