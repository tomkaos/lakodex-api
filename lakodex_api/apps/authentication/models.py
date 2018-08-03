from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models, transaction
from lakodex_api.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, username, password=None):

        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        if username is None:
            raise TypeError('Superusers must have a username')

        if password is None:
            raise TypeError('Superusers must have a password')

        if email is None:
            raise TypeError('Superusers must have an email')

        user = self.create_user(email, first_name=first_name, last_name=last_name, username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):

    username = models.CharField(db_index=True, max_length=30, unique=True)
    email = models.EmailField(db_index=True, max_length=40, unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
