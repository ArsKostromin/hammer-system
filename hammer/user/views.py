import random
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import CustomUser
from .serializers import PhoneSerializer, SMSCodeSerializer, UserProfileSerializer, PhoneLoginSerializer, VerifyLoginCodeSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView


User = get_user_model()

class RequestPhoneView(APIView):
    '''генерация и отправка кода для подтверждения'''
    def post(self, request: Request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            username = serializer.validated_data['username']
            password = make_password(serializer.validated_data['password'])
            email = serializer.validated_data['email']

            #генерируем 4-значный код
            sms_code = str(random.randint(1000, 9999))
            cache.set(
                f'user_data_{phone_number}', 
                {
                    'sms_code': sms_code,
                    'username': username,
                    'email': email,
                    'password': password
                },
                timeout=300  # 5 минут
            )
            #имитация отправки смски
            time.sleep(2)
            print(f'Код для {phone_number}: {sms_code}')

            return Response({'message': f'Код отправлен на ваш номер {sms_code};^)'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VerifySMSCodeView(APIView):
    def post(self, request: Request): 
        serializer = SMSCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            sms_code = serializer.validated_data['sms_code']

            # Получаем данные из кэша
            cached_data = cache.get(f'user_data_{phone_number}')
            if cached_data is None:
                return Response({'message': 'Неверный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Проверяем код
            if cached_data['sms_code'] != sms_code:
                return Response({'message': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

            # Извлекаем данные пользователя из кэша
            username = cached_data['username']
            email = cached_data['email']
            password = cached_data['password']

            # Создаем пользователя
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={
                    'username': username,
                    'email': email,
                    'password': password,
                }
            )

            return Response({
                'message': 'Код подтвержден',
                'user_created': created,
                'profile_url': f'/api/profile/{user.id}/'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
            
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        
        # Проверяем, передан ли инвайт-код
        invite_code = data.get('activated_invite_code') 
        if invite_code:
            # проеряем существует ли пользователь с таким инвайт кодом
            try:
                inviter = User.objects.get(invite_code=invite_code)
            except User.DoesNotExist:
                return Response({'detail': 'Инвайт-код недействителен'}, status=status.HTTP_400_BAD_REQUEST)

            if user.activated_invite_code:
                return Response({'detail': f'У вас уже активирован инвайт-код: {user.activated_invite_code}'}, status=status.HTTP_400_BAD_REQUEST)
            
            # активируем код и добавляем приглашённых
            user.activated_invite_code = invite_code
            user.save()

            inviter.invitees.add(user)
            inviter.save()
        
        return super().update(request, *args, **kwargs)
                   
            
class RequestLoginCodeView(APIView):
    def post(self, request: Request):
        serializer = PhoneLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            # Проверяем существование пользователя
            try:
                user = User.objects.get(phone_number=phone_number)
                if not user.check_password(password):
                    return Response({'message': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'Пользователь с таким номером не существует'}, status=status.HTTP_400_BAD_REQUEST)

            # Генерация и сохранение кода
            sms_code = str(random.randint(1000, 9999))
            cache.set(
                f'login_code_{phone_number}', 
                {
                    'sms_code': sms_code,
                },
                timeout=300  # 5 минут
            )
            # Имитация отправки смс
            time.sleep(2)
            print(f'Код для {phone_number}: {sms_code}')
            
            return Response({'message': 'Код отправлен на ваш номер'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyLoginCodeView(APIView):
    def post(self, request: Request):
        serializer = VerifyLoginCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            sms_code = serializer.validated_data['sms_code']

            # Получаем данные из кэша
            cached_data = cache.get(f'login_code_{phone_number}')
            if not cached_data:
                return Response({'message': 'Код истек или не был отправлен'}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем код
            cached_code = cached_data['sms_code']
            if cached_code != sms_code:
                return Response({'message': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем пользователя
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({'message': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)

            # Генерация токенов
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Успешный вход в аккаунт'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



