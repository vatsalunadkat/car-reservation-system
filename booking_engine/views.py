# This file contains the functions (i.e. logic) for the Booking API calls.
#
#
# Booking can have the following status values:
# 1. INIT - Booking has be initialized in the backend.
# 2. FAILED - Booking has failed due to invalid user or no vehicles available or other.
# 3. CONFIRMED - Booking has been confirmed successfully.
# 4. INPROGRESS - Booking is in progress. After the mentioned datestamp (Can be added later on using DB triggers or CRON JOB)
# 6. COMPLETED -  Booking has completed full cycle. User has retured the vehicle. Vehicle status to be set as available.
#
# @author Vatsal Unadkat
# @date 09 Sept, 2022
# @copyright None

# Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .serializers import BookingSerializer
from user_register.serializers import UserSerializer
from vehicle_register.serializers import VehicleSerializer

from .models import Booking
from user_register.models import User
from vehicle_register.models import Vehicle

import jwt
import datetime

# Create your views here.


class RegisterBookingView(APIView):
    def post(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        # TODO Check if user is authorized to fetch such details

        # Check if user is valid
        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user.'})

        # Check if vehicle is available
        vehicle = Vehicle.objects.filter(
            licence_number=request.data['licence_number'], available=True).first()

        if vehicle is None:
            return Response({'status': 'FAILED', 'data': 'This vehicle is invalid. (Invalid or does not exist.)'})

        vehicle_serialized = VehicleSerializer(vehicle)

        # Check no current bookings
        booking_check = Booking.objects.filter(
            user=payload['id'], booking_status='CONFIRMED').first()

        if booking_check is not None:
            return Response({'status': 'FAILED', 'data': 'This user alredy has a confirmed book. Please complete previous booking to make a new one'})

        request.data['user'] = payload['id']
        request.data['vehicle'] = vehicle_serialized.data['id']
        request.data['booking_status'] = 'CONFIRMED'
        request.data['booking_datetime'] = datetime.datetime.utcnow()

        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Set vehicle status to unavailabe
        vehicle_data = {'available': False}

        vehicle_update = VehicleSerializer(
            instance=vehicle, data=vehicle_data, partial=True)
        vehicle_update.is_valid(raise_exception=True)
        vehicle_update.save()

        return Response({'status': 'SUCCESS', 'message': 'Booking registered successfully.', 'data': serializer.data})


class RetrieveBookingView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        serialized_user = UserSerializer(user)

        # Change here
        booking = Booking.objects.filter(
            user=payload['id'], booking_status='CONFIRMED').first()

        if booking is None:
            return Response({'status': 'FAILED', 'message': 'This user has no bookings'})

        serializer = BookingSerializer(booking)
        serialized_data = serializer.data

        # TODO Convert datetime to more human readable format
        # serialized_data['booking_datetime'] = serialized_data['booking_datetime'].strftime(
        #     '%m/%d/%Y, %H:%M:%S')

        # Adding user detials
        serialized_data['user'] = serialized_user.data

        # Fetch details of the vehicle and serilize it
        vehicle = VehicleSerializer(Vehicle.objects.filter(
            id=serialized_data['vehicle']).first())

        if vehicle is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid vehicle ID.'})

        serialized_data['vehicle'] = vehicle.data

        return Response({'status': 'SUCCESS', 'message': 'Booking details fetched successfully.', 'data': serialized_data})


class UpdateBookingView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        booking = Booking.objects.filter(
            user=payload['id'], booking_status='CONFIRMED').first()

        if booking is None:
            return Response({'status': 'FAILED', 'data': 'This user has no confirmed bookings'})

        serializer = BookingSerializer(
            instance=booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': 'SUCCESS', 'message': 'Booking updated successfully.', 'data': serializer.data})


class CancelBookingView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Token not found. Session may have expired. Please login again.'})

        # TODO Check if user is authorized to fetch such details

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        booking = Booking.objects.filter(
            user=payload['id'], booking_status='CONFIRMED').first()

        if booking is None:
            return Response({'status': 'FAILED', 'message': 'This user has no bookings'})

        serializer = BookingSerializer(booking)
        serialized_data = serializer.data

        serialized_data['booking_status'] = 'CANCELLED'

        serializer_save = BookingSerializer(
            instance=booking, data=serialized_data, partial=True)
        serializer_save.is_valid(raise_exception=True)
        serializer_save.save()

        return Response({'status': 'SUCCESS', 'message': 'Booking cancelled successfully.', 'data': serializer_save.data})
