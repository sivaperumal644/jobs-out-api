from django.db import models


class State(models.Model):
    """State model for users and jobs"""

    state_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.state_name


class District(models.Model):
    """District model for users and jobs"""

    district_name = models.CharField(max_length=255, null=False, blank=False)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.district_name
