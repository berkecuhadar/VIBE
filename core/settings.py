import os
from pathlib import Path
from dotenv import load_dotenv  # python-dotenv kütüphanesini içe aktarıyoruz

BASE_DIR = Path(__file__).resolve().parent.parent

# .env dosyasındaki değişkenleri işletim sistemi ortamına (os.environ) yükler
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Gizli anahtarı ve DEBUG modunu os.environ üzerinden güvenle çekiyoruz
SECRET_KEY = os.environ.get('SECRET_KEY')

# os.environ verileri string döndürdüğü için True/False kontrolü yapıyoruz
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Host Configuration
ALLOWED_HOSTS = ["*"]
if not DEBUG:
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', '*')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'vibe',
    
    # Authentication & Social Accounts
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILE MANAGEMENT ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# --- AUTH CONFIGURATION ---
SITE_ID = 1
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- ALLAUTH & DISCORD SETTINGS ---
SOCIALACCOUNT_PROVIDERS = {
    'discord': {
        'SCOPE': ['identify', 'guilds', 'guilds.members.read'],
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_ALLOW_REGISTRATION = False 
SOCIALACCOUNT_AUTO_SIGNUP = True 
ACCOUNT_LOGIN_METHODS = {'username'}
ACCOUNT_SIGNUP_FIELDS = [] 
ACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'