from .base import *

#####################
# Security settings #
#####################

SECRET_KEY = '<fake-secret-key>'

DEBUG = True

ALLOWED_HOSTS = ['*']

################
# Static files #
################

STATIC_ROOT = BASE_DIR / 'static_root'
# MEDIA_ROOT = BASE_DIR / 'media_root'
MEDIA_ROOT = BASE_DIR / 'media'

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
        # 開発用
        'development': {
            'format': '[{name}] {asctime} [{levelname}] {pathname}:{lineno:d} '
                      '{message}',
            'style': '{',
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'development',
        },
    },
    # ルートロガー
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    # その他のロガー
    'loggers': {
        # 自作アプリケーションごとにロガーを定義することも可能
        'ctf': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Django本体が出力するログ全般を扱うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するためのロガー
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
}

########################
# Django Debug Toolbar #
########################

if DEBUG:
    def show_toolbar(request):
        return True


    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
