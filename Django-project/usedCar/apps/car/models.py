from django.db import models

# Create your models here.
from apps.user.models import User

FOR_CHOICES = (
    ('true', '是'),
    ('false', '否'),
)

FOR_EXAMINE = (
    ('1', '审核中'),
    ('2', '审核通过'),
    ('3', '审核不通过'),
)


class Brand(models.Model):
    logo_brand = models.ImageField(upload_to='logo', null=True, verbose_name='品牌logo')
    btitle = models.CharField(max_length=30, null=False, verbose_name='品牌')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        ordering = ["-id"]
        db_table = 'Brand'
        verbose_name = '车辆品牌表'
        verbose_name_plural = verbose_name


class Carinfo(models.Model):
    carbrand = models.ForeignKey(Brand, null=True, verbose_name='车辆品牌')
    user = models.ForeignKey(User, verbose_name='用户')

    picture = models.ImageField(upload_to='car', verbose_name='照片')

    model = models.CharField(max_length=30, null=False, verbose_name='车辆型号')
    regist_date = models.DateField(default=False, verbose_name='上牌日期')
    engineNo = models.CharField(max_length=30, null=False, verbose_name='发动机号')
    mileage = models.IntegerField(default=10, verbose_name='公里数')
    isService = models.CharField(choices=FOR_CHOICES, default='false', max_length=10, verbose_name='维修记录')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='期望售价')
    newprice = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='新车价格')
    formalities = models.CharField(choices=FOR_CHOICES, default='true', max_length=10, verbose_name='手续')
    isDebt = models.CharField(choices=FOR_CHOICES, default='false', max_length=10, verbose_name='债务')
    promise = models.TextField(null=True, verbose_name='卖家承诺')

    examine = models.CharField(max_length=30, choices=FOR_EXAMINE, default='1', verbose_name='审核进度')

    isPurchase = models.BooleanField(default=False, verbose_name='是否购买')
    extractprice = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='成交价格')

    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        ordering = ["-id"]
        db_table = 'Carinfo'
        verbose_name = '车辆信息表'
        verbose_name_plural = verbose_name
