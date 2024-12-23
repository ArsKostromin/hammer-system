import requests

# Базовый URL вашего API
BASE_URL = "http://127.0.0.1:8000"

# Данные для запроса RequestPhoneView
phone_data = {
    "phone_number": "+1234567890",
    "username": "test_user1",
    "password": "secure_password_123",
    "email": "test_user@example.com"
}

# Отправляем запрос на RequestPhoneView
request_phone_url = f"{BASE_URL}/users/request-phone/"
response = requests.post(request_phone_url, json=phone_data)

if response.status_code == 200:
    print("Код успешно отправлен.")
    # Запрашиваем код у пользователя
    sms_code = input("Введите код, отправленный на телефон: ")

    # Данные для запроса VerifySMSCodeView
    verify_data = {
        "phone_number": phone_data["phone_number"],
        "sms_code": str(sms_code)
    }

    # Отправляем запрос на VerifySMSCodeView
    verify_sms_url = f"{BASE_URL}/users/verify-sms/"
    verify_response = requests.post(verify_sms_url, json=verify_data)

    if verify_response.status_code == 200:
        print("Пользователь успешно создан.")
        print("Ответ от сервера:", verify_response.json())
    else:
        print("Ошибка при проверке кода:", verify_response.json())
else:
    print("Ошибка при отправке данных:", response.json())
