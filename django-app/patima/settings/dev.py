from .base import *

DEBUG = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': '3306',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]
SECRET_KEY = 'sde3)x9oad(n+xx436j)*==8b#a5rsz3-es96xdz!n3*h(3gs*'
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY
ALLOWED_HOSTS = ['*']
