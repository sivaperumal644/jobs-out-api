import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from general.models import District, Profession, State


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creating and saving a user"""
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not extra_fields["phone_number"]:
            raise ValueError("Phone number is required")
        if not extra_fields["first_name"]:
            raise ValueError("First name is required")
        if len(password) < 8:
            raise ValueError("Password must be atleast 8 characters long")

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
            first_name=first_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    gender_choices = [("M", "Male"), ("F", "Female"), ("O", "Others")]
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    experience = models.IntegerField(null=True, blank=True)
    other_skills = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["phone_number", "first_name"]

    def __str__(self):
        """Returns String representation of the model"""
        return self.email
