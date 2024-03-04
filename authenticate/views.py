from django.shortcuts import render
from .models import User
from .serializer import RegisterSerializer, UserSerializer, UserUpdateserializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from django.middleware import csrf
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import tokens
from rest_framework import decorators, permissions as rest_permissions


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return ({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token)
    })


@decorators.permission_classes([rest_permissions.AllowAny])
class RegisterViews(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(validated_data=request.data)
            user.generate_otp()
            self.send_email(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, request, user):
        otp = user.generate_otp()
        subject = "Verification OTP"

        verification_otp = reverse('verify', args={otp})

        otp_part = verification_otp.split('/')[-2]

        message = f'Hi,{user.first_name}+" "+{user.last_name},\n'\
            f'Here is your verification otp:-{otp_part}\n'\
            f'ThankYou for using our application'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@decorators.permission_classes([rest_permissions.IsAuthenticated])
class UpdateUserView(APIView):
    def put(self, request, id=None):
        user = User.objects.get(id=id)
        serializer = UserUpdateserializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.permission_classes([rest_permissions.AllowAny])
class VerifyView(APIView):
    def get(self, request, otp):
        user = self.get_user_otp(otp)

        if user:
            user.is_active = True
            user.verification_otp = None
            self.send_email(request, user)
            user.save()
            return Response("User Email Verified Successfully", status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(
                "Incorrect OTP", status=status.HTTP_400_BAD_REQUEST)

    def get_user_otp(self, otp):
        try:
            user = User.objects.get(verification_otp=otp, is_active=False)
            return user
        except User.DoesNotExist:
            return None

    def send_email(self, request, user):
        subject = "Confermation Mail"

        message = f'Hi,{user.first_name}+{user.last_name},\n'\
            f'Your account is successfully verified\n'\
            f'Thank You'

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@decorators.permission_classes([rest_permissions.AllowAny])
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User Not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        response = Response()
        token = get_token(user)

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=token["refresh_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.data = {
            "message": "login successfully",
            "access_token": token['access_token'],
            "resfresh_token": token['refresh_token']
        }

        response["CSRFToken"] = csrf.get_token(request)

        return response


@decorators.permission_classes([rest_permissions.IsAuthenticated])
class UserView(APIView):
    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@decorators.permission_classes([rest_permissions.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        response = Response()

        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        )
        token = tokens.RefreshToken(refresh_token)

        token.blacklist()

        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response.delete_cookie('X-CSRFToken')
        response.delete_cookie('csrftoken')

        response['X-CSRFToken'] = None
        response.data = {
            "message": "user logout successfully"
        }
        return response


@decorators.permission_classes([rest_permissions.AllowAny])
class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                f"The email {email} is not registered or is already active.")

        otp = user.generate_otp()

        if self.send_email(request, user):
            return Response("New OTP was send to the registered email.", status=status.HTTP_200_OK)
        else:
            return Response("Some thing went wrong.", status=status.HTTP_400_BAD_REQUEST)

    def send_email(self, request, user):
        otp = user.verification_otp
        subject = "Verification OTP Resent"

        message = f'Hi,{user.first_name}+{user.last_name},\n'\
            f'Here is your new otp for verification :- {otp}\n'\
            f'ThankYou.'

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
