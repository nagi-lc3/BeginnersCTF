# Generated by Django 3.2.7 on 2021-09-24 21:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0006_alter_problem_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='answer',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='正しい入力方式で入力してください。', regex='^ctf\\{[\\w]+\\}$')], verbose_name='問題解答'),
        ),
    ]