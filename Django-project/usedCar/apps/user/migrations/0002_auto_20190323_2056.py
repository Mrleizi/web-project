# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-23 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=150, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(max_length=11, null=True, verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='user',
            name='realname',
            field=models.CharField(max_length=50, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uidentity',
            field=models.CharField(max_length=18, null=True, verbose_name='身份证'),
        ),
    ]
