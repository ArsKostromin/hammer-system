from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import ActivateInviteCodeView, SendCodeView, VerifyCodeView, ProfileView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('activated_invite_code/', ActivateInviteCodeView.as_view(), name='ac_inv_code'),
    path('auth/send_code/', SendCodeView.as_view(), name='send_code'),
    path('auth/verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/', ProfileView.as_view(), name='profile'),
    ]