from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STUDIO_OWNER = "S"
    EMPLOYEE = "E"
    CUSTOMER = "C"
    MEMBERSHIP_CHOICES = [
        (STUDIO_OWNER, 'studio_owner'),
        (EMPLOYEE, 'employee'),
        (CUSTOMER, 'customer')
    ]
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    type = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=CUSTOMER)

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.email
