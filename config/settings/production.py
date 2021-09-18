from .base import *

#####################
# Security settings #
#####################

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

################
# Static files #
################

STATIC_ROOT = f'/var/www/{BASE_DIR.name}/static'
MEDIA_ROOT = f'/var/www/{BASE_DIR.name}/media'

###########
# Logging #
###########

LOGGING = {
    # スキーマバージョンは「1」固定
    'version': 1,
    # すでに作成されているロガーを無効化しないための設定
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 本番用
        'production': {
            'format': '{asctime} <{process:d},{thread:d}> [{levelname}] '
                      '{pathname}:{lineno:d} {message}',
            'style': '{',
        },
    },
    # ハンドラ
    'handlers': {
        # ファイル出力用ハンドラ
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'/var/log/{BASE_DIR.name}/app.log',
            'formatter': 'production',
        },
    },
    # ルートロガー
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    # その他のロガー
    'loggers': {
        # Django本体が出力するログ全般を扱うロガー
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

###################
# Stripe settings #
###################

# Stripe 公開可能キー
# STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
# Stripe シークレットキー
# STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
