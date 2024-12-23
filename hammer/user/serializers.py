from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)  # Номер телефона
    username = serializers.CharField(max_length=32, allow_blank=True, required=False)  # Имя пользователя
    password = serializers.CharField(
        max_length=128, 
        write_only=True, 
        validators=[validate_password]  # Проверка сложности пароля
    )
    email = serializers.EmailField(required=False, validators=[validate_email])  # Email
class SMSCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)  # Номер телефона
    sms_code = serializers.CharField(max_length=4)       # Код из SMS

        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'invite_code', 'activated_invite_code']