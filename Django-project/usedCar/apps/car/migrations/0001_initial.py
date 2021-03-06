# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-23 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_brand', models.ImageField(default='brandlogo.png', upload_to='logo', verbose_name='品牌logo')),
                ('btitle', models.CharField(max_length=30, verbose_name='品牌')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'verbose_name': '车辆品牌表',
                'verbose_name_plural': '车辆品牌表',
                'db_table': 'Brand',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Carinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='car', verbose_name='照片')),
                ('model', models.CharField(max_length=30, verbose_name='车辆型号')),
                ('regist_date', models.DateField(default=False, verbose_name='上牌日期')),
                ('engineNo', models.CharField(max_length=30, verbose_name='发动机号')),
                ('mileage', models.IntegerField(default=10, verbose_name='公里数')),
                ('isService', models.CharField(choices=[('true', '是'), ('false', '否')], default='false', max_length=10, verbose_name='维修记录')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='期望售价')),
                ('newprice', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='新车价格')),
                ('formalities', models.CharField(choices=[('true', '是'), ('false', '否')], default='true', max_length=10, verbose_name='手续')),
                ('isDebt', models.CharField(choices=[('true', '是'), ('false', '否')], default='false', max_length=10, verbose_name='债务')),
                ('promise', models.TextField(null=True, verbose_name='卖家承诺')),
                ('examine', models.CharField(choices=[('1', '审核中'), ('2', '审核通过'), ('3', '审核不通过')], default='1', max_length=30, verbose_name='审核进度')),
                ('isPurchase', models.BooleanField(default=False, verbose_name='是否购买')),
                ('extractprice', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='成交价格')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('carbrand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='car.Brand', verbose_name='车辆品牌')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户')),
            ],
            options={
                'verbose_name': '车辆信息表',
                'verbose_name_plural': '车辆信息表',
                'db_table': 'Carinfo',
                'ordering': ['-id'],
            },
        ),
    ]
