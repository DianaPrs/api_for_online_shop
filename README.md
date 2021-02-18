# Дипломный проект по курсу «Django: создание функциональных веб-приложений»

API для интернет-магазина. 
API сервиса и интерфейс администрирования. 
В качестве фреймворка Django и Django REST Framework.

Описание API
-------------------

Сущности:

Товар
url: /api/v1/products/

Отзыв к товару
url: /api/v1/product-reviews/

Заказы
url: /api/v1/orders/

Подборки
url: /api/v1/product-collections/

Регистрация пользователя:
url: /api/v1/auth/users/

Получение токена:
url: /api/v1/auth-token/token/login/


Установка
--------------

Для загрузки репозитория выполните в консоли:
```
git clone https://github.com/DianaPrs/api_for_online_shop.git
```
Создайте и активируйте виртуальное окужение:
```
python3 -m venv env
```
команда активации для Linux и Mac:
```
source env/bin/activate
```
для Windows:
```
env\Scripts\activate
```
Установите пакеты:
```
pip install -r requirements.txt
```

Настройка
---------------
Создайте файл settings_local.py с настройками:
```
import os
from .settings import BASE_DIR

SECRET_KEY = 'YOUR_SECRET_KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'online_shop_db',
        'USER': 'YOUR_USERNAME',
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': 'YOUR_HOST',
        'PORT': 'YOUR_PORT',
    }
}
```

Создайте базу в postgres и проведите миграцию:
```
manage.py migrate
```
Загрузите тестовые данные:
```
python manage.py loaddata fixtures.json
```
Запуск
---------
Запустите отладочный веб-сервер проекта:
```
python manage.py runserver
```