import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Create your models here.

class UserProfileManger(BaseUserManager):

    def create_user(self, email=None, password=None, **kwargs_arguments):
        if email is None:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email=email.lower()),
                          userame=self.normalize_email(email=email.lower()),
                          **kwargs_arguments)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None, **kwargs_arguments):
        if password is None:
            raise TypeError("Password field is required")
        user = self.create_user(email, password, **kwargs_arguments)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(editable=False, auto_created=True, default=uuid.uuid4(), primary_key=True)
    username = models.CharField(max_length=200, unique=False, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True, db_index=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    objects = UserProfileManger()
    USERNAME_FIELD = 'email'




class Referral(models.Model):
    id = models.UUIDField(editable=False, auto_created=True, default=uuid.uuid4(), primary_key=True)
    user = models.ForeignKey(User, related_name='referral_user', on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    date_created= models.DateField(auto_now_add=True)

