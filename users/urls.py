from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet
from .views import UserListView, RegisterView, LoginView, UserView, LogoutView, UpdateUserView

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls), name="all_users"),
    # path('', UserListView.as_view(), name="all_users"),
    path('user', UserView.as_view(), name="user_profile"),
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('update', UpdateUserView.as_view(), name="update"),
]
