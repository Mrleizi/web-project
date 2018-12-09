#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/12/3 10:56
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : forms.py
# @Software: pycharm
from django import forms

from article.models import Category


class ArticleForm(forms.Form):
    # 文章验证
    title = forms.CharField(required=True, max_length=50)
    content = forms.CharField(widget=forms.Textarea)
    keywords = forms.CharField(required=True, max_length=50)
    describe = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.CharField(required=True)
    tags = forms.CharField(required=True)
    titlepic = forms.ImageField(required=False)
    visibility = forms.CharField(required=True)

    def clean_category(self):
        category_test = self.cleaned_data['category']
        category = Category.objects.filter(id=category_test).first()
        if category:
            return category
        raise forms.ValidationError('该栏目不存在')


class CategoryForm(forms.Form):
    name = forms.CharField(required=True)
    alias = forms.CharField()
    fid = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    describe = forms.CharField(widget=forms.Textarea)
