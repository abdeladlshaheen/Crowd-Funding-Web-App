from asyncio.windows_events import NULL
from decimal import Decimal
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, UserRateProject
from .serializers import PictureSerializer, ProjectSerializer, TagSerializer, UserDonationSerializer, UserRateProjectSerializer
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

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
        pictures = request.data.pop(
            'pictures', None) if 'pictures' in request.data else []
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

        for picture in pictures:
            picture_serializer = PictureSerializer(
                data={'project': project_serializer.data['id'], 'picture': picture})
            picture_serializer.is_valid(raise_exception=True)
            picture_serializer.save()

        return Response(project_serializer.data)


class RateProjectView(APIView):
    def post(self, request, id):
        project_id = id if get_object_or_404(Project, pk=id) else None
        rate = request.data['rate']
        user_id = Auth.authenticate(request)['id']
        user_rate_project = UserRateProject.objects.filter(
            user=user_id, project=project_id).first()
        if user_rate_project:
            serializer = UserRateProjectSerializer(
                user_rate_project, data={'rate': rate}, partial=True)
        else:
            serializer = UserRateProjectSerializer(
                data={'rate': rate, 'user': user_id, 'project': project_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": serializer.data})

# total_target
# donations
# user


def cancel_project(request, project_id):
    user_id = Auth.authenticate(request)['id']
    project = get_object_or_404(Project, pk=project_id)
    res = Response()
    if check_cancel_project(project.donations, project.total_target) and project.user_id == user_id:
        Project.objects.filter(pk=project_id).update(is_canceled=True)
        return HttpResponse(json.dumps({'success': 'Project Is Canceled Successfully'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'fail': 'This project Can\'t be canceled'}), content_type="application/json")


def check_cancel_project(donnation, total):
    return donnation < (Decimal('0.25') * total)


def related_projects(project):
    related = []
    project_tags = Project.objects.filter(
        id=project.id).values_list('tags', flat=True)

    projects = Project.objects.all()
    for pro in projects:
        tags = Project.objects.filter(id=pro.id).values_list('tags', flat=True)

        if set(tags).intersection(project_tags):
            related.append(pro)

    return related


class ProjectDetails(APIView):
    def get(self, request, id):
        project = Project.objects.get(pk=id)
        # pics
        related = related_projects(project)
        picture = project.picture_set.all().values_list('picture', flat=True)
        # rate
        #TODO: average
        rate = project.userrateproject_set.all().values_list('rate', flat=True)
        # donation
        donation = project.projectdonation_set.all().values_list('donation', flat=True)

        # serializers
        project_serializer = ProjectSerializer(project)

        related_serializer = ProjectSerializer(related, many=True)
        # wrap all serializers in one object
        context = {
            "project": project_serializer.data,
            "picture": picture,
            "donation": donation,
            "rate": rate,
            "related": related_serializer.data
        }
        return Response(data=context)
