from .base import *

DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost"
]

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '3306',
    }
}
print(os.getenv('DB_USER'))
SECRET_KEY = os.getenv('SECRET_KEY')

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY
