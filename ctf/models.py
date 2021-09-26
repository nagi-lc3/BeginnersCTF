from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


class Problem(models.Model):
    """問題モデル"""

    class Meta:
        db_table = 'problem'
        verbose_name = verbose_name_plural = '問題'

    answer_regex = RegexValidator(regex=r'^ctf\{[\w]+\}$', message='正しい入力方式で入力してください。')

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
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    name = models.CharField(verbose_name='問題名', max_length=50)
    file = models.FileField(verbose_name='問題ファイル', upload_to='problems/', null=True, blank=True)
    statement = models.TextField(verbose_name='問題文')
    genre = models.CharField(verbose_name='問題ジャンル', choices=GENRE, max_length=50)
    level = models.IntegerField(verbose_name='問題難易度', choices=LEVEL)
    score = models.IntegerField(verbose_name='問題得点')
    answer = models.CharField(verbose_name='問題解答', validators=[answer_regex], max_length=50)
    created_at = models.DateTimeField(verbose_name='問題作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='問題更新日時', auto_now=True)

    # UserProblemテーブルとPersonテーブルの間にUserProblem中間テーブル
    custom_user = models.ManyToManyField(get_user_model(), through='UserProblem')

    def __str__(self):
        return self.name


class UserProblem(models.Model):
    """ユーザ問題モデル（中間テーブル）"""

    class Meta:
        db_table = 'user_problem'
        verbose_name = verbose_name_plural = 'ユーザ問題'
        unique_together = ['custom_user', 'problem']

    # リレーション
    custom_user = models.ForeignKey(get_user_model(), verbose_name='ユーザ名', on_delete=models.PROTECT)
    problem = models.ForeignKey(Problem, verbose_name='問題名', on_delete=models.PROTECT)

    problem_correct_answer = models.BooleanField(verbose_name='問題正解', default=0)
    corrected_at = models.DateTimeField(verbose_name='問題正解日時', null=True, blank=True)


class Information(models.Model):
    """お知らせモデル"""

    class Meta:
        db_table = 'information'
        verbose_name = verbose_name_plural = 'お知らせ'

    title = models.CharField(verbose_name='お知らせタイトル', max_length=50)
    contents = models.TextField(verbose_name='お知らせ内容')
    created_at = models.DateTimeField(verbose_name='お知らせ作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='お知らせ更新日時', auto_now=True)

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    """お問い合わせモデル"""

    class Meta:
        db_table = 'inquiry'
        verbose_name = verbose_name_plural = 'お問い合わせ'

    name = models.CharField(verbose_name='名前', max_length=50)
    email = models.EmailField(verbose_name='メールアドレス')
    subject = models.CharField(verbose_name='お問い合わせ件名', max_length=50)
    contents = models.TextField(verbose_name='お問い合わせ内容')
    created_at = models.DateTimeField(verbose_name='お問い合わせ日時', auto_now_add=True)

    def __str__(self):
        return self.subject
