from django.db import models


class State(models.Model):
    """State model for users and jobs"""

    state_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.state_name
