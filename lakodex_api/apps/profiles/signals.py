from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver

from lakodex_api.apps.authentication.models import User
from lakodex_api.apps.core.utils import create_avatar_url

from .models import Profile


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, **kwargs):

    if created:
        profile = Profile.objects.create(user=instance)
        email = instance.email
        avatar_url = create_avatar_url(email)
        profile.image = avatar_url
        profile.save()


@receiver(user_signed_up)
def callback_after_social_signup(request, user, **kwargs):

    data = SocialAccount.objects.filter(user=user)

    if (data):
        picture = data[0].get_avatar_url()
        if picture:
            Profile.objects.filter(user=user).update(image=picture)
