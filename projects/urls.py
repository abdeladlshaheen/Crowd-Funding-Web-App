from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet
from .views import CreateProjectView, DonationView, ProjectDetails, ProjectListView, RateProjectView, cancel_project, CommentListAPIView, comment_project_api, get_latest_five_projects, get_highest_five_projects


router = routers.DefaultRouter()
router.register('', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProjectListView.as_view()),
    path('create', CreateProjectView.as_view()),
    path('<int:id>/rate', RateProjectView.as_view()),
    path('<int:project_id>/cancel', cancel_project),
    path('<int:id>', ProjectDetails.as_view()),
    path('donate/<int:id>', DonationView.as_view()),
    path('comments', CommentListAPIView.as_view()),
    path('comment/<int:id>', comment_project_api),
    path('latestfive', get_latest_five_projects),
    path('topfive', get_highest_five_projects),
]
