""" accounts App model. """

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Model representing a user profile.
    """

    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.PROTECT
    )
    description = models.TextField(blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username
