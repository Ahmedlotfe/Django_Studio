from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt

import datetime
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from users.models import User
from .models import Employee, Studio, Reservation, StudioOwner
from .serializers import StudioSerializer, ReservationSerializer


def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("UnAuthenticated")
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("UnAuthenticated")

    user = User.objects.get(pk=payload['id'])
    return user


class CreateStudio(APIView):
    def post(self, request):
        user = get_user(request)

        # Check if the user is a studio owner or not
        if user.studio_owner.all().count() <= 0:
            return Response({"message": "You Are not a studio owner"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        studio_owner = user.studio_owner.all().first()
        data["studio_owner"] = studio_owner.id
        studio_serializer = StudioSerializer(data=data)
        if studio_serializer.is_valid(raise_exception=True):
            studio_serializer.save()

        return Response(studio_serializer.data)


class AddEmployeesToStudio(APIView):
    def post(self, request):
        user = get_user(request)

        # Check if the user is a studio owner or not
        if user.studio_owner.all().count() <= 0:
            return Response({"message": "You Are not a studio owner"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        employee_ids = data['employee_ids']

        # looping through the employees ids and set their studios
        for id in employee_ids:
            employee = Employee.objects.get(pk=id)
            studio = Studio.objects.get(pk=data['studio_id'])

            # Check the studio owner is the user who send the request
            if user.studio_owner.all().first() != studio.studio_owner:
                return Response({"message": "You Are not the studio owner"}, status=status.HTTP_403_FORBIDDEN)
            else:
                employee.studio = studio
                employee.save()
        return Response({"message": "Employees added"})


class CreateReservation(APIView):
    def post(self, request):
        user = get_user(request)

        # Check if the user is a Customer or not
        if user.customer.all().count() <= 0:
            return Response({"message": "You Are not a Customer"}, status=status.HTTP_403_FORBIDDEN)

        studio = Studio.objects.get(pk=request.data['studio'])
        today = datetime.date.today()

        # Get all reservations today for specific studio
        reservations = Reservation.objects.filter(
            Q(created_at=today) & Q(studio=studio))

        # Check if the number of reservations exceeds the allowed number
        if len(reservations) >= 3:
            return Response({"message": "Reservations completed today"}, status=status.HTTP_403_FORBIDDEN)

        customer = user.customer.all().first()
        data = request.data
        data["customer"] = customer.id

        reservation_serializer = ReservationSerializer(data=data)
        if reservation_serializer.is_valid(raise_exception=True):
            reservation_serializer.save()

        return Response(reservation_serializer.data)


class CancelReservation(APIView):
    def post(self, request):
        user = get_user(request)

        # Check if the user is a Customer or not
        if user.customer.all().count() <= 0:
            return Response({"message": "You Are not a Customer"}, status=status.HTTP_403_FORBIDDEN)

        current_customer = user.customer.all().first()
        reservation = Reservation.objects.get(
            pk=request.data['reservation_id'])

        if current_customer == reservation.customer:
            time_now = timezone.now()
            duration = time_now - reservation.created_time
            if timedelta(hours=0, minutes=15, seconds=0) > duration:
                reservation.delete()
                return Response({"message": "Your reservation has been canceled"})
            else:
                return Response({"message": "You have exceeded the time available to cancel"})

        return Response({"message": "Your not the reservation owner"}, status=status.HTTP_403_FORBIDDEN)


class ReservationsList(APIView):
    def get(self, request):
        user = get_user(request)

        # Check if the user is a Customer
        if user.customer.all().count() > 0:
            current_customer = user.customer.all().first()
            reservations = Reservation.objects.filter(
                customer=current_customer)

            reservation_serializer = ReservationSerializer(
                reservations, many=True)
            return Response(reservation_serializer.data)

        # Check if the user is an Employee
        elif user.employee.all().count() > 0:
            current_employee = Employee.objects.get(employee=user)
            studio = current_employee.studio
            reservations = Reservation.objects.filter(
                studio=studio)

            reservation_serializer = ReservationSerializer(
                reservations, many=True)
            return Response(reservation_serializer.data)

        # Check if the user is a Studio Owner
        elif user.studio_owner.all().count() > 0:
            studio_owner = StudioOwner.objects.get(owner=user)
            reservations = Reservation.objects.filter(
                studio__studio_owner=studio_owner)

            reservation_serializer = ReservationSerializer(
                reservations, many=True)
            return Response(reservation_serializer.data)

        # Check if the user is an admin user
        elif user.is_superuser:
            reservations = Reservation.objects.all()
            reservation_serializer = ReservationSerializer(
                reservations, many=True)
            return Response(reservation_serializer.data)
