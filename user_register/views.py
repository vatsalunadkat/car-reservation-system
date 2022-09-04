# This file contains the functions (i.e. logic) for the User API calls.
#
# @author Vatsal Unadkat
# @date 09 Sept, 2022
# @copyright None

# Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .serializers import UserSerializer
from .models import User

import jwt
import datetime

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'SUCCESS', 'message': 'User registered successfully.', 'data': serializer.data})


class AuthenticateView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # .first() is used here as the email feild is unique
        user = User.objects.filter(email=email).first()

        # Check if user exists in the DB
        if user is None:
            # We do NOT clearly specify that ONLY the password is incorrect for security reasons.
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Incorrect email or password. Please try again.'})

        # Check for password (after decoding)
        if not user.check_password(password):
            # We do NOT clearly specify that ONLY the password is incorrect for security reasons.
            raise AuthenticationFailed(
                {'status': 'FAILED', 'message': 'Incorrect email or password. Please try again.'})

        # Token expires in 60 min = 1 hr
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'Status': 'SUCCESS',
            'jwt': token
        }

        return response


class WhoAmIView(APIView):
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

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response({'status': 'SUCCESS', 'message': 'User data retrieved successfully.', 'data': serializer.data})


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'status': 'SUCCESS', 'message': 'Logout success.'}
        return response


class RetrieveView(APIView):
    def get(self, request, id):
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

        user = User.objects.filter(id=id).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        serializer = UserSerializer(user)

        return Response({'status': 'SUCCESS', 'data': serializer.data})


class RetrieveAllView(APIView):
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

        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return Response({'status': 'SUCCESS', 'data': serializer.data})


class UpdateView(APIView):
    def post(self, request, id):
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

        user = User.objects.filter(id=id).first()

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        serializer = UserSerializer(
            instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'SUCCESS', 'data': serializer.data})


class DeleteView(APIView):
    def delete(self, request, id):
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

        user = User.objects.get(id=id)

        if user is None:
            raise ValidationError(
                {'status': 'FAILED', 'message': 'Invalid user ID.'})

        user.delete()

        return Response({'status': 'SUCCESS', 'message': 'Item deleted successfully!'})
