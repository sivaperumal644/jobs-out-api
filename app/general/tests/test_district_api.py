from django.test import TestCase
from django.urls import reverse
from general import models
from rest_framework import status
from rest_framework.test import APIClient

DISTRICT_URL = reverse("general:districts")


def create_state(**params):
    return models.State.objects.create(**params)


def create_district(**params):
    return models.District.objects.create(**params)


class DistrictAPITests(TestCase):
    """Test the districts API"""

    def setUp(self):
        self.client = APIClient()

        state_one = {"state_name": "Tamil Nadu"}
        state_two = {"state_name": "Kerala"}

        first_state = create_state(**state_one)
        second_state = create_state(**state_two)

        district_one = {
            "district_name": "Coimbatore",
            "state_id": first_state,
        }
        district_two = {"district_name": "Chennai", "state_id": second_state}

        create_district(**district_one)
        create_district(**district_two)
        
        return super().setUp()

    def test_get_all_districts(self):
        """Tests get all Districts API"""
        res = self.client.get(DISTRICT_URL)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data["districts"]), 2)
