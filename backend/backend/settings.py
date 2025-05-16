import os
from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url

# Путь к базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = config('SECRET_KEY')

# Режим отладки
DEBUG = True

# Установленные приложения
INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Требуется для django-allauth
    'rest_framework',
    'rest_framework.authtoken',  # Оставляем для совместимости
    'corsheaders',  # Для CORS
    'dj_rest_auth',  # Для JWT-токенов
    'rest_framework_simplejwt',  # Для JWT-токенов
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',  # Для регистрации
    'allauth.socialaccount',  # Для социальной аутентификации
]

# Настройки социальной аутентификации (пустой словарь для минимальной конфигурации)
SOCIALACCOUNT_PROVIDERS = {}

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Настройки dj-rest-auth
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh',
    'JWT_AUTH_HTTPONLY': True,  # Для доступа фронтенда к токенам
    'REGISTER_SERIALIZER': 'main.serializers.CustomRegisterSerializer',
}

# Настройки Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Настройки django-allauth
SITE_ID = 1  # Требуется для django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Отправляем письмо, но не требуем подтверждения
ACCOUNT_AUTHENTICATION_METHOD = 'username'  # Аутентификация по имени пользователя
ACCOUNT_ADAPTER = 'main.adapters.CustomAccountAdapter'  # Кастомный адаптер для отправки писем
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Agile Task Planning App] '
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1', 'password2', 'first_name', 'last_name', 'display_name'] 
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False  # Не ждем подтверждения для входа

ACCOUNT_RATE_LIMITS = {
    'login_failed': None  # Отключаем лимит попыток входа
}
# Настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Настройки CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Адрес React-приложения
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Для CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Для django-allauth
]

# URL-конфигурация
ROOT_URLCONF = 'backend.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'backend.wsgi.application'


# База данных (PostgreSQL)
import dj_database_url

# Базовые настройки Django
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Настройка базы данных через DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://postgres:Alfapostgre2608@localhost:5432/agile_db')

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agile_db',
        'USER': 'postgres',
        'PASSWORD': 'Alfapostgre2608',
        'HOST': 'localhost',
        'PORT': '5432',
        }
} 
DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:Alfapostgre2608@db:5432/agile_db')
}
'''

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = 'static/'

# Настройки аутентификации
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"
AUTH_USER_MODEL = 'main.CustomUser'

# Тип первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'