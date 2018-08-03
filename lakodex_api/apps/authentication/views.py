from __future__ import unicode_literals
from django.conf import settings

from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, GenericAPIView

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.adapter import get_adapter as get_social_adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount import signals

from rest_auth.registration.views import SocialLoginView, SocialConnectView
from rest_auth.registration.serializers import SocialConnectSerializer

from .serializers import CustomSocialAccountSerializer
from lakodex_api.apps.core.utils import import_attribute


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def PasswordCheckView(request):
    user = request.user
    password = 'false'

    if (user.has_usable_password()):
        password = 'true'

    return Response(password)


class SocialAccountListView(ListAPIView):

    serializer_class = CustomSocialAccountSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)


class SocialAccountDisconnectView(GenericAPIView):
    """
    Disconnect SocialAccount from remote service for
    the currently logged in user
    """
    serializer_class = SocialConnectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        accounts = self.get_queryset()
        account = accounts.filter(pk=kwargs['pk']).first()
        if not account:
            raise NotFound

        social_adapter = import_attribute(settings.SOCIALACCOUNT_ADAPTER)
        social_adapter.validate_disconnect(self, account, accounts)

        account.delete()
        signals.social_account_removed.send(
            sender=SocialAccount,
            request=self.request,
            socialaccount=account
        )

        return Response(self.get_serializer(account).data)
