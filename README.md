# Дипломный проект по курсу «Django: создание функциональных веб-приложений»

API для интернет-магазина. 
API сервиса и интерфейс администрирования. 
В качестве фреймворка Django и Django REST Framework.


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