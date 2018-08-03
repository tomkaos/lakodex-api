from django.db import models

from lakodex_api.apps.core.models import TimestampedModel

from lakodex_api.apps.authentication.models import User


class Profile(TimestampedModel):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )

    phone = models.CharField(blank=True, max_length=30)

    image = models.URLField(blank=True)

    job_title = models.CharField(blank=True, max_length=30)

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    def __str__(self):
        return self.user.email

    # Follow `profile` if we're not already following `profile`
    def follow(self, profile):
        self.follows.add(profile)

    # Unfollow `profile` if we're already following `profile`
    def unfollow(self, profile):
        self.follows.remove(profile)

    # Returns True if we're following `profile`; False otherwise.
    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()

    # Returns True if `profile` is following us; False otherwise.
    def is_followed_by(self, profile):
        return self.follows.filter(pk=profile.pk).exists()
