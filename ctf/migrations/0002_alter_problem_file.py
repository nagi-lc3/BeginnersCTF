# Generated by Django 3.2.7 on 2021-09-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='file',
            field=models.FileField(upload_to='problems/', verbose_name='問題ファイル'),
        ),
    ]