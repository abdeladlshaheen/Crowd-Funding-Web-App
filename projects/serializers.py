from rest_framework import serializers
from .models import Project, Picture, Comment, Tag, UserRateProject, Rate


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class UserRateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRateProject
        fields = "__all__"
