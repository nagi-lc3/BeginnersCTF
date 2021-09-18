from django.conf import settings
from django.db import models


class Problem(models.Model):
    """問題モデル"""

    class Meta:
        db_table = 'problem'
        verbose_name = verbose_name_plural = '問題'

    GENRE = (
        ('crypto', 'Crypto'),
        ('forensics', 'Forensics'),
        ('reversing', 'Reversing'),
        ('pwnable', 'Pwnable'),
        ('web', 'Web'),
        ('network', 'Network'),
        ('misc', 'Misc'),
    )

    LEVEL = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    name = models.CharField(verbose_name='問題名', max_length=255)
    file = models.FileField(verbose_name='問題ファイル')
    statement = models.CharField(verbose_name='問題文', max_length=4095)
    genre = models.CharField(verbose_name='問題ジャンル', choices=GENRE, max_length=255)
    level = models.IntegerField(verbose_name='問題難易度', choices=LEVEL)
    score = models.IntegerField(verbose_name='問題得点')
    answer = models.CharField(verbose_name='問題解答', max_length=255)

    custom_user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UsersProblem')

    def __str__(self):
        return self.name


class UsersProblem(models.Model):
    """ユーザ問題モデル（中間テーブル）"""

    class Meta:
        db_table = 'users_problem'
        verbose_name = verbose_name_plural = 'ユーザ問題'

    custom_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    problem_correct_answer = models.BooleanField(verbose_name="問題正解", default=0)