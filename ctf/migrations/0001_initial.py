# Generated by Django 3.2.7 on 2021-09-18 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='問題名')),
                ('file', models.FileField(upload_to='', verbose_name='問題ファイル')),
                ('statement', models.CharField(max_length=4095, verbose_name='問題文')),
                ('genre', models.CharField(choices=[('crypto', 'Crypto'), ('forensics', 'Forensics'), ('reversing', 'Reversing'), ('pwnable', 'Pwnable'), ('web', 'Web'), ('network', 'Network'), ('misc', 'Misc')], max_length=255, verbose_name='問題ジャンル')),
                ('level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='問題難易度')),
                ('score', models.IntegerField(verbose_name='問題得点')),
                ('answer', models.CharField(max_length=255, verbose_name='問題解答')),
            ],
            options={
                'verbose_name': '問題',
                'verbose_name_plural': '問題',
                'db_table': 'problem',
            },
        ),
        migrations.CreateModel(
            name='UsersProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_correct_answer', models.BooleanField(default=0, verbose_name='問題正解')),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.problem')),
            ],
            options={
                'verbose_name': 'ユーザ問題',
                'verbose_name_plural': 'ユーザ問題',
                'db_table': 'users_problem',
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='custom_user',
            field=models.ManyToManyField(through='ctf.UsersProblem', to=settings.AUTH_USER_MODEL),
        ),
    ]
