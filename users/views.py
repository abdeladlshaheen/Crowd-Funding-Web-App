from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from .serializers import UserSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from .models import User
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django_email_verification import send_email

import jwt
import datetime
import os

from rest_framework import generics, status
from .utils import Util
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect


class Auth:
    def authenticate(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        return payload

    def check_status(request):
        token = request.COOKIES.get('jwt')
        if token:
            try:
                # check if the token has expired
                # if it cannot be decoded successfully, it means that token has expired
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                raise AuthenticationFailed("You are already logged in!")
            except jwt.ExpiredSignatureError:
                pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListView(APIView):
    # TODO: AttributeError: Got AttributeError when attempting to get a value for field `title` on serializer `ProjectSerializer`.
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request):
        payload = Auth.authenticate(request)
        user = get_object_or_404(User, pk=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GetUserView(APIView):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        if user.is_superuser or user.is_staff:
            raise AuthenticationFailed("Unauthenticated!")
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        Auth.check_status(request)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data['email'])
        send_email(user)

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        Auth.check_status(request)

        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User Not Found!")

        if password != user.password:
            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect Password!")

        if not user.is_active:
            raise AuthenticationFailed(
                'You have to verify your account first!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }
        user.last_login = datetime.datetime.utcnow()
        user.save()
        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token,
            "last_login": user.last_login
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        payload = Auth.authenticate(request)
        if payload:
            response.delete_cookie('jwt')
            message = "Logged out successfully!"
        else:
            message = "You are not logged in!"
        response.data = {
            "detail": message
        }
        return response


class UpdateUserView(APIView):
    def put(self, request):
        payload = Auth.authenticate(request)
        user = get_object_or_404(User, pk=payload['id'])

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
