import os
from pathlib import Path
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['jjsystem.onrender.com','127.0.0.1','localhost']
CSRF_TRUSTED_ORIGINS = ['https://jjsystem.onrender.com/']



MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ProductosServicios',
    'ServicioTecnico',
    'Envios',
    'Pqrsf',
    'Account'
]

AUTHENTICATION_BACKENDS = ['Account.backends.UsuariosBackend']
LOGIN_URL = 'login'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jjsystemPrueba.urls'

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

WSGI_APPLICATION = 'jjsystemPrueba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://jjsystem_db_user:6dMP0YFLSFZDvZwgbL7lVp0dMG1joGbF@dpg-coa92bcf7o1s73dme92g-a.oregon-postgres.render.com:5432/jjsystem_db_ujbz'
        )  
    # 'default': dj_database_url.config(
    #     # Replace this value with your local database's connection string.
    #     default='mysql://root:1021662854@localhost:3306/jjsystem_db',
    #     conn_max_age=600
    # )
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'jjsystem_db',
    #     'USER': 'root',
    #     'PASSWORD': '1021662854',
    #     #'PASSWORD': '',
    #     'HOST': 'localhost',
    #     'PORT': '3306'
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_FROM_EMAIL = 'jjsystemproject@gmail.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jjsystemproject@gmail.com'
EMAIL_HOST_PASSWORD = 'oybttoqvhrehynlq'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'ServicioTecnico', 'static'),
    os.path.join(BASE_DIR, 'Account', 'static'),
    os.path.join(BASE_DIR, 'ProductosServicios', 'static'),
    os.path.join(BASE_DIR, 'Pqrsf', 'static'),
    os.path.join(BASE_DIR, 'Envios', 'static'),
]

MEDIA_ROOT = [os.path.join(BASE_DIR, 'ServicioTecnico'),
            os.path.join(BASE_DIR, 'Account'),
            os.path.join(BASE_DIR, 'ProductosServicios'),
            os.path.join(BASE_DIR, 'Pqrsf'),
            os.path.join(BASE_DIR, 'Envios'),]
MEDIA_URL = 'images/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
# Suprimir todas las advertencias relacionadas con la asignación de números a instancias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
