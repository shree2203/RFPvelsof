from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = extra_fields['first_name'] + extra_fields['last_name']
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_approved_by_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class VendorDetails(models.Model):
    CATEGORY_CHOICE = [
        ('abc', '1'),
        ('abcd', '2'),
        ('abcss', '3'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    total_employees = models.IntegerField(default=0)
    gst_no = models.CharField(max_length=15, default="", blank=False)
    pan_no = models.CharField(max_length=10, default="", blank=False)
    phn_no = models.CharField(max_length=10, default='0000000000')
    categories = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICE,
        default='1'
    )


class Approval(models.Model):
    vendor = models.OneToOneField(VendorDetails, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
