from rest_framework import serializers
from .models import User
from django_countries.serializer_fields import CountryField


class UserSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = User
        fields = "__all__"
