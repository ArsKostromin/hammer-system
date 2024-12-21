from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import CustomUser
from .serializers import CustomUserSerializer, ProfileSerializer, PhoneNumberSerializer, VerifyCodeSerializer
import random
import time
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.request import Request


User = get_user_model()

# class AuthView(APIView):
#     def get(self, request: Request):
        


# class SendCodeView(APIView):
#     """Первый запрос: отправка 4-значного кода на указанный номер телефона."""
#     def post(self, request):
#         serializer = PhoneNumberSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']

#             # Генерация 4-значного кода
#             code = f"{random.randint(1000, 9999)}"
#             print(code)

#             # Сохраняем код в кэше с TTL 5 минут
#             cache.set(f"auth_code_{phone_number}", code, timeout=300)

#             # Имитация отправки SMS (задержка 2 секунды)
#             time.sleep(2)
#             print(f"Code sent to {phone_number}: {code}")

#             return Response({"message": "Код отправлен!"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyCodeView(APIView):
#     """Второй запрос: проверка кода и создание пользователя, если он новый."""

#     def post(self, request):
#         serializer = VerifyCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             code = serializer.validated_data['code']

#             # Проверка кода
#             cached_code = cache.get(f"auth_code_{phone_number}")
#             if cached_code != code:
#                 return Response({"error": "Неверный или истекший код."}, status=status.HTTP_400_BAD_REQUEST)

#             # Создание пользователя, если его нет
#             user, created = User.objects.get_or_create(phone_number=phone_number, defaults={
#                 'username': f"user_{phone_number}",
#                 'invite_code': generate_invite_code(),
#             })

#             # Возвращаем профиль и токен
#             return Response({
#                 "message": "Успешная авторизация.",
#                 "profile": ProfileSerializer(user).data
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(APIView):
#     """Получение профиля пользователя."""

#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)
#         return Response({"error": "Не авторизован."}, status=status.HTTP_401_UNAUTHORIZED)


# class ActivateInviteCodeView(APIView):
#     def post(self, request):
#         user = request.user
#         invite_code = request.data.get('invite_code')

#         if not invite_code:
#             return Response({"error": "Не указан инвайт-код."}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user.activate_invite_code(invite_code)
#             return Response({"message": "Инвайт-код успешно активирован."}, status=status.HTTP_200_OK)
#         except ValidationError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

