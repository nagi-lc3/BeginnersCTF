# Generated by Django 3.2.7 on 2021-09-21 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0012_auto_20210921_2122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userproblem',
            options={'verbose_name': 'ユーザ問題', 'verbose_name_plural': 'ユーザ問題'},
        ),
        migrations.RemoveConstraint(
            model_name='userproblem',
            name='unique_stock',
        ),
        migrations.AlterModelTable(
            name='userproblem',
            table='user_problem',
        ),
    ]