from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from .manager import CustomUserManager

# def profile_picture_upload_path(instance, filename):
#     return f"user/{instance.id}/profile_picture/{filename}"

# def default_icon_image():
#     return "user/default/account.png"

class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = models.CharField(_("username"), max_length=30, unique=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile")
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)
    phone_number = PhoneNumberField(blank=False, unique=True)
    date_of_birth = models.DateField() # add validation for dob serializer
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = PhoneNumberField(blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"