from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls), name="all_users"),
]
