from django.urls import path, include
from .views import CreateProjectView, ProjectDetails, ProjectListView, RateProjectView
from rest_framework import routers
from .views import ProjectViewSet

router = routers.DefaultRouter()
router.register('', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', ProjectListView.as_view()),
    path('create', CreateProjectView.as_view()),
    path('<int:id>/rate', RateProjectView.as_view()),
    path('<int:id>', ProjectDetails.as_view())
]
