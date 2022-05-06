from rest_framework import serializers
from .models import Project, Picture, Comment, ProjectDonation, Tag, UserRateProject


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class UserRateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRateProject
        fields = "__all__"


class UserDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDonation
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    # nested serializers
    # SlugRelatedField

    tags = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True
    )

    category = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )

    class Meta:
        model = Project
        fields = "__all__"
