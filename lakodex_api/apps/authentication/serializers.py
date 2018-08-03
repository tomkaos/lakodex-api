from collections import OrderedDict
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import HyperlinkedModelSerializer

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.models import SocialAccount

from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import JWTSerializer

from lakodex_api.apps.profiles.serializers import ProfileSerializer
from lakodex_api.apps.profiles.models import Profile

from .models import User


class CustomSocialAccountSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = SocialAccount
        fields = (
            'id',
            'provider',
            'image',
            'uid',
            'last_login',
            'date_joined',
        )

    def get_image(self, obj):
        avatar_image = obj.get_avatar_url()
        if avatar_image:
            return avatar_image
        return ''


class CustomModelSerializer(HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context:
            self._context = getattr(self.Meta, 'context', {})
        try:
            self.user = self.context['request'].user
        except KeyError:
            self.user = None

    def get_fields(self):
        ret = OrderedDict()

        fields = super().get_fields()

        for f in fields:
            ret[f] = fields[f]

        return ret


class UserSerializer(CustomModelSerializer):

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'profile', 'created_at', 'updated_at')
        read_only_fields = ('email', 'created_at')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        user = super(UserSerializer, self).update(instance, validated_data)

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)

        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            user = self._validate_email(email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(
                        email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(
                        _('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=30,
        min_length=6,
        required=True
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    profile = ProfileSerializer(read_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_username(self, username):
        user_model = get_user_model()  # your way of getting the User
        try:
            user_model.objects.get(username__iexact=username)
        except user_model.DoesNotExist:
            return username
        raise serializers.ValidationError(
            _("A user is already registered with this username."))

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.username = self.cleaned_data.get('username')
        user.save()
        return user


class CustomJWTSerializer(JWTSerializer):

    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user_data = UserSerializer(obj['user'], context=self.context).data
        return user_data
