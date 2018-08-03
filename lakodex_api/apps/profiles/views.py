from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Profile
from lakodex_api.apps.authentication.models import User
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileDetailsView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):

        try:
            email = User.objects.get(username__iexact=username)
            profile = self.queryset.get(user__email=email)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this email does not exists.')

        serializer = self.serializer_class(profile, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
