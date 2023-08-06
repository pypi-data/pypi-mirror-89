import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from unchained_utils.v0.base_classes import LowerCaseEmailField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise TypeError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    username = None
    first_name = None
    last_name = None
    email = LowerCaseEmailField('email address', unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
