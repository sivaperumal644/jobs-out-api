from django.db import models


class State(models.Model):
    """State model for users and jobs"""

    state_name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.state_name


class District(models.Model):
    """District model for users and jobs"""

    district_name = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.district_name


class Profession(models.Model):
    """Profession model for users"""

    profession_name = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )

    def __str__(self) -> str:
        return self.profession_name
