import random
import time
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import CustomUser
from .serializers import PhoneSerializer, SMSCodeSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password


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

            
            
class UserProfileView(APIView):
    def get(self, request: Request, user_id):            
            try:
                user = User.objects.get(id=user_id)
                Serializer = UserProfileSerializer(user)
                return Response(Serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)