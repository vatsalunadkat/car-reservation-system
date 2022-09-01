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


class LoginView(APIView):
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
