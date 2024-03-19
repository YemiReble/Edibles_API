from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as GT
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class AccountManager(BaseUserManager):


    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(GT('Enter a valid email address.'))


    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(GT('An Email is required.'))
        email = self.normalize_email(email)
        self.email_validator(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(GT('This user must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(GT('This user must have is_superuser=True.'))
        if extra_fields.get('is_admin') is not True:
            raise ValueError(GT('This user must be set to Admin=True'))
        user = self.create_user(email, password, **extra_fields)
        user.save(using=self._db)
