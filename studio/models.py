from django.db import models
from users.models import User


class StudioOwner(models.Model):
    owner = models.ForeignKey(
        User, related_name='studio_owner', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.owner.username


class Studio(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    studio_owner = models.ForeignKey(
        StudioOwner, related_name='studio', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee = models.ForeignKey(
        User, related_name='employee', on_delete=models.CASCADE)
    studio = models.ForeignKey(
        Studio, related_name='employee', on_delete=models.CASCADE, null=True)


class Customer(models.Model):
    customer = models.ForeignKey(
        User, related_name='customer', on_delete=models.CASCADE)


class Reservation(models.Model):
    customer = models.ForeignKey(
        Customer, related_name='reservation', on_delete=models.CASCADE, null=True)
    studio = models.ForeignKey(
        Studio, related_name='reservation', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)
