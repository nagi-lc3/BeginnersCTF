# Generated by Django 3.2.7 on 2021-09-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(default='icon/default.jpg', upload_to='icon/', verbose_name='ユーザアイコン'),
        ),
    ]
