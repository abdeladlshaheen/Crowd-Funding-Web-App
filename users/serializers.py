from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password',
                  'mobile_phone',
                  'profile_picture',
                  'birthday',
                  'fb_profile',
                  'country')
