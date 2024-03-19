from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as GT
from .manager import AccountManager
from django.db import models
from uuid import uuid4
import datetime



class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    email = models.EmailField(max_length=300, verbose_name=GT('Email Address'), unique=True)
    first_name = models.CharField(max_length=200, verbose_name=GT('First Name'))
    last_name = models.CharField(max_length=200, verbose_name=GT('Last Name'))
    username = models.CharField(max_length=200, verbose_name=GT('User Name'))
    phone_number = models.CharField(max_length=200, verbose_name=GT('Phone Number'))
    password = models.CharField(max_length=200, verbose_name=GT('Password'))
    user_permissions = models.ManyToManyField(Permission, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = AccountManager()

    
    def __str__(self):
        return self.email


class OneTimePassword(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(Account, related_name="activationtoken", on_delete=models.CASCADE)
    token = models.CharField(GT("Token"), max_length=4, null=False, blank=False)
    timer = models.DateTimeField(null=False, blank=False)
    date_issued = models.DateTimeField(auto_now_add=True, null=False, blank=False)


    def __str__(self):
        return f"{self.token}"
