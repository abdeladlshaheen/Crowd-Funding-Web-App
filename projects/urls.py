import imp
from django.urls import path, include
from .views import CreateProjectView, ProjectDetails, ProjectListView, RateProjectView, CommentListAPIView, CommentDetailAPIView
from rest_framework import routers
from .views import ProjectViewSet
from django.urls import re_path

router = routers.DefaultRouter()
router.register('', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProjectListView.as_view()),
    path('create', CreateProjectView.as_view()),
    path('<int:id>/rate', RateProjectView.as_view()),
    path('<int:id>', ProjectDetails.as_view()),
    #path("comment/<int:pid>", Comment.as_view(), name="comment"),
    re_path(r'^comments/$', CommentListAPIView.as_view(), name='List'), 
    re_path(r'^comments/(?P<id>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
]   
