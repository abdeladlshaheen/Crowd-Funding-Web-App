from django.urls import path, include
from rest_framework import routers
from .views import CreateProjectView, DonationView, ProjectDetails, ProjectListView, RateProjectView, cancel_project, CommentListAPIView, comment_project_api


urlpatterns = [
    path('', ProjectListView.as_view()),
    path('create', CreateProjectView.as_view()),
    path('<int:id>/rate', RateProjectView.as_view()),
    path('<int:project_id>/cancel', cancel_project),
    path('<int:id>', ProjectDetails.as_view()),
    path('donate/<int:id>', DonationView.as_view()),
    path('comments', CommentListAPIView.as_view()),
    path('comment/<int:id>', comment_project_api),
 
]
