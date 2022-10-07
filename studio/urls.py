from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello, name="say_hello"),
    path("create/", views.CreateStudio.as_view()),
    path("add_employees/", views.AddEmployeesToStudio.as_view()),
    path("reserve/", views.CreateReservation.as_view()),
    path("cancel_reservation/", views.CancelReservation.as_view()),
    path("list_reservations/", views.ReservationsList.as_view()),
]
