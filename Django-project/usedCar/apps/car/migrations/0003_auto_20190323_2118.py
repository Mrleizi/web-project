# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-23 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_auto_20190323_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='extractprice',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='成交价格'),
        ),
    ]
