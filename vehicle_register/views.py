from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .serializers import VehicleSerializer
from .models import Vehicle
from user_register.models import User
import jwt
import datetime

# Create your views here.


class RegisterVehicleView(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RetrieveVehicleView(APIView):
    def get(self, request, id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                'Invalid User ID.')

        vehicle = Vehicle.objects.filter(id=id).first()

        if vehicle is None:
            raise ValidationError(
                'Invalid Vehicle ID.')

        serializer = VehicleSerializer(vehicle)

        return Response(serializer.data)


class UpdateVehicleView(APIView):
    def post(self, request, id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                'Invalid User ID.')

        vehicle = Vehicle.objects.filter(id=id).first()

        if vehicle is None:
            raise ValidationError(
                'Invalid Vehicle ID.')

        serializer = VehicleSerializer(
            instance=vehicle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DeleteVehicleView(APIView):
    def delete(self, request, id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                'Invalid User ID.')

        vehicle = Vehicle.objects.filter(id=id).first()

        if vehicle is None:
            raise ValidationError(
                'Invalid Vehicle ID.')

        vehicle.delete()

        return Response('Item successfully deleted!')
