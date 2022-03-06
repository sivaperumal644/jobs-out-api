from django.test import TestCase
from general import models


class ModelTest(TestCase):
    def test_create_state(self):
        """Test Create State with string representation"""
        state = models.State.objects.create(state_name="Tamil Nadu")
        self.assertEquals(str(state), state.state_name)
