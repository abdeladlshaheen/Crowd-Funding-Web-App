from rest_framework import serializers
from .models import User
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            # 'email': {
            #     'read_only': True
            # }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        instance = self.Meta.model(
            **validated_data,
            # TODO: Direct assignment to the forward side of a many-to-many set is prohibited. Use groups.set() instead.
            # groups=groups,
            # user_permissions=user_permissions,
        )
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
