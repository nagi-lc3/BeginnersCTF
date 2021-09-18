import environ
from pathlib import Path

###############
# Build paths #
###############

BASE_DIR = Path(__file__).resolve().parent.parent.parent

###############
# env #
###############

env = environ.Env()
# Read .env if exists
environ.Env.read_env(str(BASE_DIR / '.env'))

############
# Security #
############

DEBUG = False

ALLOWED_HOSTS = []

#################
# Core settings #
#################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps

    # My applications
    'accounts.apps.AccountsConfig',
    'ctf.apps.CtfConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

##################
# Authentication #
##################

# AUTH_USER_MODEL = 'accounts.CustomUser'
#
# LOGIN_REDIRECT_URL = '/shop/'


############
# Database #
############

DATABASES = {
    'default': env.db()
}
DATABASES['default']['TIME_ZONE'] = 'Asia/Tokyo'
DATABASES['default']['ATOMIC_REQUESTS'] = True
# DATABASES['default']['OPTIONS']['sql_mode'] = 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO'

#######################
# Password validation #
#######################

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

########################
# Internationalization #
########################

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

################
# Static files #
################

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'

#######################
# Other core settings #
#######################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##################
# django-tables2 #
##################

# DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"


###################
# Stripe settings #
###################

# Stripe 公開可能キー
# STRIPE_PUBLISHABLE_KEY = '<stripe-publishable-key>'
# Stripe シークレットキー
# STRIPE_SECRET_KEY = '<stripe-api-secret-key>'
