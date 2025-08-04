# users/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, identifier, name, password=None):
        if not identifier:
            raise ValueError("Users must provide an email or phone number")

        if '@' in identifier:
            user = self.model(email=identifier, name=name)
        else:
            user = self.model(phone=identifier, name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, name, password):
        user = self.create_user(identifier, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # we'll accept both but email is used internally
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email if self.email else self.phone
