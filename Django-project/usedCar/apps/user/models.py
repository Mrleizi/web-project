from django.db import models

# Create your models here.

SEX_CHOICES = (
    ('1', '男'),
    ('0', '女'),
)


class User(models.Model):
    username = models.CharField(max_length=255, null=False, verbose_name='用户名')
    userpwd = models.CharField(max_length=255, null=False, verbose_name='密码')

    realname = models.CharField(max_length=50, null=True, verbose_name='姓名')
    sex = models.CharField(choices=SEX_CHOICES, default='1', max_length=10, verbose_name='性别')
    cellphone = models.CharField(max_length=11, null=True, verbose_name='手机')
    uidentity = models.CharField(max_length=18, null=True, verbose_name='身份证')
    address = models.CharField(max_length=150, null=True, verbose_name='地址')

    class Meta:
        db_table = 'Users'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name
