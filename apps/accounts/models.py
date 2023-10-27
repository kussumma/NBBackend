from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid
from tools.filestorage_helper import GridFSStorage


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_active") is not True:
            raise ValueError("Superuser must be active")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **kwargs)


LEVEL_CHOICES = [
    ("bronze", "Bronze"),
    ("silver", "Silver"),
    ("gold", "Gold"),
    ("platinum", "Platinum"),
]


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    avatar = models.ImageField(
        storage=GridFSStorage(collection="avatars"),
        default="default.jpg",
        db_index=True,
    )
    level = models.CharField(choices=LEVEL_CHOICES, max_length=20, default="bronze")
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=False, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


GENDER_CHOICES = [("male", "Male"), ("female", "Female")]


class UserDetail(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    user = models.OneToOneField(
        User, related_name="user_details", on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, default="female")
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)
    newsletter = models.BooleanField(default=False, db_index=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, default="EN", db_index=True)
    theme = models.CharField(max_length=255, default="light")
    currency = models.CharField(max_length=255, default="IDR")

    def __str__(self):
        return f"{self.user.email} - {self.gender}"
