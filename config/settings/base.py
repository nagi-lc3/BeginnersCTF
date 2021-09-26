import environ
from pathlib import Path

###############
# Build paths #
###############
from django.contrib import messages

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
    'jazzmin',  # 管理サイトのデザイン
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_boost',
    'import_export',
    'django_tables2',
    'bootstrap5',
    'django_cleanup',

    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',

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

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_REDIRECT_URL = 'account_login'

############
# Database #
############

DATABASES = {
    'default': env.db()
}
DATABASES['default']['TIME_ZONE'] = 'Asia/Tokyo'
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['sql_mode'] = 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO'
# DATABASES['default']['init_command'] = 'STRICT_TRANS_TABLES'

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

# メッセージタグの設定
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

#######################
# django-allauth #
#######################

# django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',  # 一般ユーザー用（メールアドレス認証）
    'django.contrib.auth.backends.ModelBackend',  # 管理サイト用（ユーザー名認証）
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# サインアップにメールアドレス確認をはさむよう設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン／ログアウト後の遷移先設定
LOGIN_REDIRECT_URL = 'ctf:problem_list'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# 送信元メールアドレス
DEFAULT_FROM_EMAIL = 'beginnersctf@gmail.com'

# コンソールにメールを送信
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# adapterをオーバーライドするための設定
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'

# バックアップパッチ用
# BACKUP_PATH = 'backup/'
# NUM_SAVED_BACKUP = 30

##################
# django-bootstrap5 #
##################

BOOTSTRAP5 = {
    'set_placeholder': False,
}

##################
# django-tables2 #
##################

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

###################
# Stripe settings #
###################

# Stripe 公開可能キー
# STRIPE_PUBLISHABLE_KEY = '<stripe-publishable-key>'
# Stripe シークレットキー
# STRIPE_SECRET_KEY = '<stripe-api-secret-key>'
