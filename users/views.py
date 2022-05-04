from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

import jwt
import datetime


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


class RegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User Not Found!")

        if password != user.password:
            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect Password!")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
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
            message ="Logged out successfully!"
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

        request.data.pop('email')   # He can edit all his data except for the email
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
