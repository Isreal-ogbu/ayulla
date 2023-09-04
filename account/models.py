import uuid
from ayullaTest import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Create your models here.

class UserProfileManger(BaseUserManager):

    def create_user(self, email=None, password=None, **kwargs_arguments):
        if email is None:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email=email.lower()),
                          username=self.normalize_email(email=email.lower()),
                          **kwargs_arguments)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None, **kwargs_arguments):
        if password is None:
            raise TypeError("Password field is required")
        user = self.create_user(email, password, **kwargs_arguments)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(editable=False, auto_created=True, default=uuid.uuid4(), primary_key=True)
    username = models.CharField(max_length=200, unique=False, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True, db_index=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserProfileManger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Email- {self.email}"

class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emailverification')
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.token)


class Referral(models.Model):
    id = models.UUIDField(editable=False, auto_created=True, default=uuid.uuid4(), primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='referral_user', on_delete=models.CASCADE)
    link = models.UUIDField(editable=False, auto_created=True, default=uuid.uuid4())
    referral_count = models.PositiveIntegerField(default=0)
    date_created= models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Link: {self.link}, Count: {self.referral_count}"

