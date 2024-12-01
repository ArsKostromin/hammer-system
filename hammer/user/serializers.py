from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'invite_code', 'activated_invite_code']
        read_only_fields = ['invite_code', 'activated_invite_code']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'invite_code', 'activated_invite_code']