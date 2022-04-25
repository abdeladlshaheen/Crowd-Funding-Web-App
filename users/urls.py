from django.urls import path, include
from rest_framework import routers
from knox import views as knox_views

from .views import UserViewSet, LoginApi

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls), name="all_users"),
    path('api/login/', LoginApi.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall')
]
