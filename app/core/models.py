from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creating and saving a user"""
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not extra_fields['phone_number']:
            raise ValueError("Phone number is required")
        if not extra_fields['first_name']:
            raise ValueError("First name is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, phone_number, first_name):
        """Creating and saving a new super user"""
        user = self.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            first_name=first_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10)
    profession = models.CharField(max_length=50)
    experience = models.IntegerField(null=True)
    other_skills = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELD = ['phone', 'first_name']
