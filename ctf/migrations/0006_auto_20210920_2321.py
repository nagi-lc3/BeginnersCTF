# Generated by Django 3.2.7 on 2021-09-20 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ctf', '0005_usersproblem_corrected_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersproblem',
            name='custom_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ名'),
        ),
        migrations.AlterField(
            model_name='usersproblem',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.problem', verbose_name='問題名'),
        ),
    ]
