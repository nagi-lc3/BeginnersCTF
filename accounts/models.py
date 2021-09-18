from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta(object):
        db_table = 'custom_user'
        verbose_name = verbose_name_plural = 'カスタムユーザー'

    score = models.IntegerField(verbose_name='ユーザ点数', default=0)
    ranking = models.IntegerField(verbose_name='ユーザランキング', null=True, blank=True)
    icon = models.ImageField(verbose_name='ユーザアイコン', null=True, blank=True)
