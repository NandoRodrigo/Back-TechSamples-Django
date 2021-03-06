from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

    now = timezone.now()

    if not email:
      raise ValueError('The given email must be set')

    email = self.normalize_email(email)

    user = self.model(
      email=email,
      is_staff=is_staff,
      is_active=True,
      is_superuser=is_superuser,
      last_login=now,
      date_joined=now,
      **extra_fields)

    user.set_password(password)

    user.save(using=self._db)

    return user

  def create_user(self, email, password=None, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractUser):

  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  is_admin = models.BooleanField()

  email = models.EmailField(max_length=255, unique=True)
  username = models.CharField(unique=False, null=True, max_length=255)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['is_admin']
