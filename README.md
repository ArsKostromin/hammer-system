●
Авторизация по номеру телефона. Первый запрос на ввод номера
телефона. Имитировать отправку 4хзначного кода авторизации(задержку
на сервере 1-2 сек). Второй запрос на ввод кода - реализовано 

●
Если пользователь ранее не авторизовывался, то записать его в бд - я сделал вход и регистрацию отдельно

●
Запрос на профиль пользователя - реализовано 

●
Пользователю нужно при первой авторизации нужно присвоить
рандомно сгенерированный 6-значный инвайт-код(цифры и символы) - реализовано 

●
В профиле у пользователя должна быть возможность ввести чужой
инвайт-код(при вводе проверять на существование). В своем профиле
можно активировать только 1 инвайт код, если пользователь уже когда-
то активировал инвайт код, то нужно выводить его в соответсвующем
поле в запросе на профиль пользователя - реализовано 

●
В API профиля должен выводиться список пользователей(номеров
телефона), которые ввели инвайт код текущего пользователя. - реализовано 

●
Реализовать и описать в readme Api для всего функционала

<hr>

http://127.0.0.1:8000/admin/user/customuser/ - админка

http://127.0.0.1:8000/users/profiles/ - все профили

http://127.0.0.1:8000/users/profile/ - твой профиль

http://127.0.0.1:8000/users/request-phone/ - регистрация, отправка данных и получение кода для подтверждения 

http://127.0.0.1:8000/users/verify-sms/ - подтверждение для регстрации

http://127.0.0.1:8000/users/login/ - вход с получением кода

http://127.0.0.1:8000/users/verify-login/ - подтверждение для входа
