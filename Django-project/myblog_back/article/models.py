from django.db import models

from user.models import User


class Category(models.Model):
    """栏目表"""
    name = models.CharField(max_length=100, unique=True, verbose_name='栏目名称')
    alias = models.CharField(max_length=100, unique=True, verbose_name='栏目别名')
    fid = models.CharField(max_length=100, null=True, verbose_name='父节点')
    keywords = models.CharField(max_length=200, null=True, verbose_name='关键字')
    describe = models.TextField(null=True, verbose_name='描述')

    class Meta:
        db_table = 'category'


class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(null=True, verbose_name='内容')
    keywords = models.CharField(max_length=50, null=True, verbose_name='关键字')
    describe = models.TextField(null=True, verbose_name='描述')

    tags = models.CharField(max_length=100, unique=True, verbose_name='标签')
    titlepic = models.ImageField(upload_to='upload', null=True, verbose_name='标题图片')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')

    visibility = models.BooleanField(default=True, verbose_name='是否公开')

    # 关联栏目表 一个栏目里面有多个文章
    category = models.ForeignKey(Category, null=False)
    author = models.ForeignKey(User, null=False)

    class Meta:
        db_table = "article"


class Comment(models.Model):
    """评论表"""
    abstract = models.TextField(verbose_name='摘要')
    time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    content = models.TextField(verbose_name='评论内容')

    article = models.ForeignKey(Article, null=True)

    class Meta:
        db_table = 'comment'
