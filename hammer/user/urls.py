from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from .views import RequestPhoneView, VerifySMSCodeView, UserProfileView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('request-phone/', RequestPhoneView.as_view(), name='request_phone'),
    path('verify-sms/', VerifySMSCodeView.as_view(), name='verify_sms'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile')    ]