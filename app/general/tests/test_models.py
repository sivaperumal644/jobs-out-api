from django.db import IntegrityError
from django.test import TestCase
from general import models


def create_sample_state():
    """Creates a sample state"""
    state = models.State.objects.create(state_name="Tamil Nadu")
    return state


class ModelTest(TestCase):
    def test_create_state(self):
        """Test Create State with string representation"""
        state = models.State.objects.create(state_name="Tamil Nadu")
        self.assertEquals(str(state), state.state_name)

    def test_duplicate_create_state(self):
        """Test Create State with same name fails"""
        create_sample_state()
        with self.assertRaises(IntegrityError):
            create_sample_state()

    def test_create_district(self):
        """Test Create District with string representation"""
        state = create_sample_state()
        district = models.District.objects.create(
            district_name="Coimbatore", state_id=state
        )
        self.assertEquals(str(district), district.district_name)
        self.assertEquals(state.id, district.state_id.id)
