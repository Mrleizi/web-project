from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 管理员表
class Admin(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    username = models.CharField(max_length=24, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=225, verbose_name='密码')
    tel = models.CharField(max_length=11, null=True, verbose_name='电话')

    class Meta:
        db_table = "administrator"


# 公告表
class Notice(models.Model):
    title = models.TextField(verbose_name='标题')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='公告发布日期')

    sender = models.ForeignKey(Admin, null=True)

    class Meta:
        db_table = 'notice'


# 登录记录表
class LoginRecord(models.Model):
    # 所有管理员和用户都有
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    login_ip = models.CharField(max_length=20, verbose_name='登录者ip')

    loginer = models.ForeignKey(Admin, null=True)

    class Meta:
        db_table = 'login_record'


# 栏目表
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='栏目名称')
    another_name = models.CharField(max_length=50, unique=True, verbose_name='栏目别名')
    keyword = models.CharField(max_length=50, null=True, verbose_name='关键字')
    describe = models.TextField(null=True, verbose_name='描述')

    class Meta:
        db_table = 'category'


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='标题')
    content = models.TextField(null=True, verbose_name='内容')
    keywords = models.CharField(max_length=50, unique=True, null=True, verbose_name='关键字')
    tags = models.CharField(max_length=50, unique=True, verbose_name='标签')
    titlepic = models.ImageField(upload_to='upload', null=True, verbose_name='标题图片')
    describe = models.TextField(null=True, verbose_name='描述')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    is_public = models.BooleanField(default=1, verbose_name='是否公开')
    # 关联栏目表 一个栏目里面有多个文章
    category = models.ForeignKey(Category, null=True)
    author = models.ForeignKey(Admin, null=True)

    class Meta:
        db_table = "article"


# 评论表
class Comment(models.Model):
    abstract = models.TextField(verbose_name='摘要')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    article = models.ForeignKey(Article, null=True)

    class Meta:
        db_table = 'comment'
