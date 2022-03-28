from django.test import TestCase
from django.urls import reverse
from general import models
from rest_framework import status
from rest_framework.test import APIClient

PROFESSION_URL = reverse("general:professions")


def create_profession(**params):
    return models.Profession.objects.create(**params)


class ProfessionAPITests(TestCase):
    """Test the profession API"""

    def setUp(self):
        self.client = APIClient()

        profession_one = {"profession_name": "Software Engineer"}
        profession_two = {"profession_name": "Doctor"}

        create_profession(**profession_one)
        create_profession(**profession_two)
        return super().setUp()

    def test_get_all_professions(self):
        """Tests get all professions API"""
        res = self.client.get(PROFESSION_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data["professions"]), 2)
