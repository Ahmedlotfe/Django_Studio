from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime

from .serializers import UserSerializer
from .models import User
from studio.serializers import StudioOwnerSerializer, EmployeeSerializer, CustomerSerializer


class RegisterView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            user_id = user_serializer.data['id']
            user = User.objects.get(pk=user_id)
            if request.data['type'] == "S":
                employee_serializer = StudioOwnerSerializer(
                    data={"owner": user.id})
                if employee_serializer.is_valid(raise_exception=True):
                    employee_serializer.save()

            elif request.data['type'] == "E":
                employee_serializer = EmployeeSerializer(
                    data={"employee": user.id})
                if employee_serializer.is_valid(raise_exception=True):
                    employee_serializer.save()

            elif request.data['type'] == "C":
                employee_serializer = CustomerSerializer(
                    data={"customer": user.id})
                if employee_serializer.is_valid(raise_exception=True):
                    employee_serializer.save()

            return Response(user_serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        # Check if the user is an employee,
        # I'm gonna create a token with studio_id which he is assigned to
        if user.employee.all().count() > 0:
            employee = user.employee.all().first()
            if employee.studio is not None:
                studio_id = employee.studio.id
                payload["studio_id"] = studio_id

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("UnAuthenticated")

        user = User.objects.get(pk=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "logout success"
        }

        return response
