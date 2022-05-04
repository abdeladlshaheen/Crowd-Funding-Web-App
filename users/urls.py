from django.urls import path, include
from rest_framework import routers
# from .views import UserViewSet
from .views import RegisterView, LoginView, UserView, LogoutView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView
from django_email_verification import urls as mail_urls
from django_email_verification import send_email

# router = routers.DefaultRouter()
# router.register('', UserViewSet)

urlpatterns = [
    # path('', include(router.urls), name="all_users"),
    path('user/', UserView().as_view(), name="user_profile"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView().as_view(), name="login"),
    path('logout/', LogoutView().as_view(), name="logout"),
    path('email/', include(mail_urls)),
    path('send_email', send_email),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
