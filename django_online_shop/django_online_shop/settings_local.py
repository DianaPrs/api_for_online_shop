import os
from .settings import BASE_DIR

SECRET_KEY = '2zzbb#x74=%dxkd*s6ep#$%&ey8j-or#3b@q0$%0df49##ic4#'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'online_shop_db',
        'USER': 'deepsee',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5001',
    }
}
