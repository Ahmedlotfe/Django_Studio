from rest_framework import serializers
from . import models


class StudioOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudioOwner
        fields = [
            'owner'
        ]


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Studio
        fields = [
            'name',
            'studio_owner'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = [
            'employee',
            'studio'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = [
            'customer'
        ]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = [
            'customer',
            'studio'
        ]
