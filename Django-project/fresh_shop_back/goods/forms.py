#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/26 9:21
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : forms.py
# @Software: pycharm

from django import forms

from goods.models import GoodsCategory


class GoodsForm(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': '商品名称必填:'})
    # 商品货号
    goods_sn = forms.CharField(required=True, error_messages={'required': '商品货号必填:'})
    # 商品库存
    goods_nums = forms.CharField(required=True, error_messages={'required': '商品库存必填:'})
    # 市场价格
    market_price = forms.CharField(required=True, error_messages={'required': '市场价格必填:'})
    # 本店价格
    shop_price = forms.CharField(required=True, error_messages={'required': '本店价格必填:'})
    # 商品简短描述
    goods_brief = forms.CharField(required=True, error_messages={'required': '商品描述必填:'})
    # 分类
    category = forms.CharField(required=True, error_messages={'required': '商品分类必填:'})
    # 商品首图
    goods_front_image = forms.ImageField(required=False)

    def clean_category(self):
        # 验证字段，返回category对象
        category_id = self.cleaned_data['category']
        category = GoodsCategory.objects.filter(category_type=category_id).first()
        if category:
            return category
        else:
            raise forms.ValidationError('商品分类选择有误')
