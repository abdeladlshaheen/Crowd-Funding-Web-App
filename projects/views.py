# from asyncio.windows_events import NULL
from datetime import datetime, timezone, tzinfo
from decimal import Decimal
import json
from django.shortcuts import render
from requests import request
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, ProjectDonation, Tag, UserRateProject, Comment
from .serializers import PictureSerializer, ProjectSerializer, TagSerializer, ProjectDonationSerializer, UserRateProjectSerializer, CommentSerializer
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from users.views import Auth
from rest_framework import viewsets
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from django.db.models import Q, Sum


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
        pictures = request.data.getlist(
            'pictures') if 'pictures' in request.data else []
        tags = request.data.getlist(
            'tags[]') if 'tags[]' in request.data else []
        tags_list = []

        # the user who creates the project must be the one who is already logged in
        payload = Auth.authenticate(request)
        request.data._mutable = True
        request.data['user'] = payload['id']
        request.data._mutable = False

        # store project data
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        project_instance = get_object_or_404(
            Project, pk=project_serializer.data['id'])

        # store multiple tags
        # if it doesn't exist, create a new one
        for tag in tags:
            stored_tag = Tag.objects.filter(name=tag).first()
            if stored_tag:
                tags_list.append(stored_tag)
            else:
                tag_serializer = TagSerializer(data={'name': tag})
                tag_serializer.is_valid(raise_exception=True)
                tag_serializer.save()

                tag_instance = get_object_or_404(
                    Tag, pk=tag_serializer.data['id'])
                tags_list.append(tag_instance)

        # assign the project for each tag entered
        for tag in tags_list:
            project_instance.tags.add(tag)

        # store multiple project pictures
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


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['comment', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comment__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
        return queryset_list


class DonationView(APIView):
    def post(self, request, id):
        # user_id, project_id, project instance & current_donation
        user_id = Auth.authenticate(request)['id']
        project_id = id if get_object_or_404(Project, pk=id) else None
        project = get_object_or_404(Project, pk=id)
        current_project_donations = ProjectDonation.objects.filter(
            project=project_id).aggregate(Sum('donation'))

        # get donation from request
        donation = request.data['donation']

        # start checking
        if Decimal(donation) < 1:
            return Response({"detail": "Making nullish or negative donation is prohibited"})

        serializer = ProjectDonationSerializer(
            data={'donation': donation, 'user': user_id, 'project': project_id})

        if project.end_time < datetime.now().replace(tzinfo=timezone.utc):
            return Response(
                {"detail": "sorry, you should not make a donation in a terminated project"})

        serializer.is_valid(raise_exception=True)

        if(current_project_donations["donation__sum"] + Decimal(serializer.validated_data["donation"]) > project.total_target):
            return Response(
                {"detail": "sorry, project total target reached"})

        serializer.save()
        return Response({"detail": serializer.data})
