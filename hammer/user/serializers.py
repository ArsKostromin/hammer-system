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
    # Поле для отображения списка приглашенных пользователей
    invitees = serializers.SerializerMethodField()
    # Поле для отображения пригласившего пользователя
    invited_by = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone_number',
            'invite_code',
            'activated_invite_code',
            'invitees',
            'invited_by',
        ]
        read_only_fields = ['invite_code', 'invitees', 'invited_by']

    def get_invitees(self, obj):
        """Возвращает список номеров телефонов пользователей, приглашенных этим пользователем."""
        return [
            invitee.phone_number.as_e164 if invitee.phone_number else None
            for invitee in obj.invitees.all()
        ]

    def get_invited_by(self, obj):
        """Возвращает номер телефона пользователя, который пригласил этого пользователя."""
        inviter = obj.invited_by.first()
        return inviter.phone_number.as_e164 if inviter and inviter.phone_number else None


class PhoneLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)  # Номер телефона
    password = serializers.CharField(
        max_length=128, 
        write_only=True, 
    )
    
    
class VerifyLoginCodeSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=4) # Код из SMS
    phone_number = serializers.CharField(max_length=15)  # Номер телефона
