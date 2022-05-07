from django.urls import re_path
from .views import ProjectViewSet
from rest_framework import routers
from .views import CreateProjectView, ProjectDetails, ProjectListView, RateProjectView, cancel_project, CommentListAPIView, comment_post_api
from .views import CreateProjectView, DonationView, ProjectDetails, ProjectListView, RateProjectView, cancel_project, CommentListAPIView
from django.urls import path, include


router = routers.DefaultRouter()
router.register('', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProjectListView.as_view()),
    path('create', CreateProjectView.as_view()),
    path('<int:id>/rate', RateProjectView.as_view()),
    path('<int:project_id>/cancel', cancel_project),
    path('<int:id>', ProjectDetails.as_view()),
    #path("comment/<int:pid>", Comment.as_view(), name="comment"),
    path('donate/<int:id>', DonationView.as_view()),
    path('comments', CommentListAPIView.as_view()),
    path('comment/<int:id>', comment_post_api),


]
