from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
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
        return Response(serializer.data)


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
                'Incorrect email or password. Please try again.')

        # Check for password (after decoding)
        if not user.check_password(password):
            # We do NOT clearly specify that ONLY the password is incorrect for security reasons.
            raise AuthenticationFailed(
                'Incorrect email or password. Please try again.')

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
            'jwt': token
        }

        return response


class RetrieveView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                'Token not found. Session may have expired. Please login again.')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout success.'
        }
        return response
