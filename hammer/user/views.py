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


User = get_user_model()

class RequestPhoneView(APIView):
    '''генерация и отправка кода для подтверждения'''
    def post(self, request: Request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            #генерируем 4-значный код
            sms_code = str(random.randint(1000, 9999))
            cache.set(f'sms_code_{phone_number}', sms_code, timeout=3000)

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
            
            cached_code = cache.get(f'sms_code_{phone_number}')
            if cached_code is None or cached_code != sms_code:
                return Response({'message': 'Неверный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Проверяем, существует ли пользователь
            user, created = User.objects.get_or_create(phone_number=phone_number)

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