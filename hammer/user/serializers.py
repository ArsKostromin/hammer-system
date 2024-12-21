from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class SMSCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    sms_code = serializers.CharField(max_length=4)
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'invite_code', 'activated_invite_code']