import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.gis.gdal import GDAL_VERSION  # GDAL versiyasini tekshirish uchun

load_dotenv()  # .env faylidagi muhit o'zgaruvchilarini yuklash

# Loyihaning asosiy papkasi yo'lini aniqlash
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti - sessiyalar va xavfsizlik uchun
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key')

# Debug rejimi - ishlab chiqish vaqtida True, serverda False bo'lishi kerak
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Ruxsat berilgan host nomlari
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# O'rnatilgan ilovalar ro'yxati
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin panel
    'django.contrib.auth',   # Autentifikatsiya tizimi
    'django.contrib.contenttypes',  # Kontent turlari uchun
    'django.contrib.sessions',      # Sessiyalar uchun
    'django.contrib.messages',      # Xabarlar tizimi
    'django.contrib.staticfiles',   # Statik fayllar uchun
    'django.contrib.gis',          # Geografik ma'lumotlar uchun
    'locations',                   # Bizning asosiy ilova
    'corsheaders',                # CORS sozlamalari uchun
]

# Middleware - so'rovlarni qayta ishlash uchun
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Xavfsizlik
    'django.contrib.sessions.middleware.SessionMiddleware', # Sessiyalar
    'corsheaders.middleware.CorsMiddleware',               # CORS
    'django.middleware.common.CommonMiddleware',           # Umumiy
    'django.middleware.csrf.CsrfViewMiddleware',           # CSRF himoyasi
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autentifikatsiya
    'django.contrib.messages.middleware.MessageMiddleware',     # Xabarlar
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking himoyasi
]

# URL'larning asosiy konfiguratsiyasi
ROOT_URLCONF = 'location_admin.urls'

# Template'lar sozlamalari
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI ilovasi uchun yo'l
WSGI_APPLICATION = 'location_admin.wsgi.application'

# Ma'lumotlar bazasi sozlamalari
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # PostGIS bilan PostgreSQL
        'NAME': os.getenv('DB_NAME'),        # Baza nomi
        'USER': os.getenv('DB_USER'),        # Foydalanuvchi
        'PASSWORD': os.getenv('DB_PASSWORD'), # Parol
        'HOST': os.getenv('DB_HOST', 'localhost'),  # Host
        'PORT': os.getenv('DB_PORT', '5432'),      # Port
    }
}

# Parol tekshirish validatorlari
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

# Til va vaqt mintaqasi sozlamalari
LANGUAGE_CODE = 'uz'           # Sayt tili
TIME_ZONE = 'Asia/Tashkent'   # Vaqt mintaqasi
USE_I18N = True               # Internatsionalizatsiya
USE_TZ = True                 # Vaqt mintaqalaridan foydalanish

# Statik fayllar sozlamalari
STATIC_URL = 'static/'        # URL manzil
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Statik fayllar papkasi

# Avtomatik ID maydoni turi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS sozlamalari
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Debug rejimida barcha so'rovlarga ruxsat
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')

# Telegram bot tokeni
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")