from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Rate, UserRateProject
from .serializers import ProjectSerializer, TagSerializer, UserRateProjectSerializer
from decimal import Decimal
from django.shortcuts import get_object_or_404

from users.views import Auth
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectListView(APIView):
    # TODO: AttributeError: Got AttributeError when attempting to get a value for field `title` on serializer `ProjectSerializer`.
    def get(self, request):
        project = Project.objects.all()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class CreateProjectView(APIView):
    def post(self, request):
        pictures = request.data.pop('pictures', None) if 'pictures' in request.data else []
        # TODO
        # tags = request.data.pop('tags', None) if 'tags' in request.data else []
        # array = []
        # array = request.data.dict()['array[]']
        # print(array)
        # print(request.data)

        # for tag in tags:
        #     tag_serializer = TagSerializer(data={'name': tag})
        #     tag_serializer.is_valid(raise_exception=True)
        #     tag_serializer.save()
        # request.data['tags'] =  
        request.data['user'] = Auth.authenticate(request)['id']
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        for i in range(len(pictures)):
            picture_serializer = PictureSerializer(
                data={'project': project_serializer.data['id'], 'picture': pictures[i]})
            picture_serializer.is_valid(raise_exception=True)
            picture_serializer.save()

        return Response(project_serializer.data)


class RateProjectView(APIView):
    def post(self, request, id):
        project_id = id if get_object_or_404(Project, pk=id) else None
        rate = request.data['rate']
        user_id = Auth.authenticate(request)['id']
        user_rate_project = UserRateProject.objects.filter(user=user_id, project=project_id).first()
        if user_rate_project:
            serializer = UserRateProjectSerializer(user_rate_project, data={'rate': rate}, partial=True)
        else:
            serializer = UserRateProjectSerializer(data={'rate': rate, 'user': user_id, 'project': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": serializer.data})
