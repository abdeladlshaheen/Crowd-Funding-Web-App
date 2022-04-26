from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView

from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response

import jwt
import datetime

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginApi(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginApi, self).post(request, format=None)
