# -*- coding: utf-8 -*-
import re

from django import forms

from apps.user.models import User


class UserRegisterForm(forms.Form):
    """
    用户注册验证表单
    """
    username = forms.CharField(required=True, max_length=20,
                               error_messages={'required': '用户名必填',
                                               'max_length': '用户名不能超过20个字符', })
    userpwd = forms.CharField(required=True, min_length=6, max_length=20,
                              error_messages={'required': '密码必填',
                                              'max_length': '密码长度不能超过20字符',
                                              'min_length': '密码长度不能短于5个字符'})
    reuserpwd = forms.CharField(required=True, min_length=6, max_length=20,
                                error_messages={'required': '确认密码必填',
                                                'max_length': '密码长度不能超过20字符',
                                                'min_length': '密码长度不能短于5个字符'})

    def clean(self):
        username = self.cleaned_data.get('username')
        userpwd = self.cleaned_data.get('userpwd')
        reuserpwd = self.cleaned_data.get('reuserpwd')
        # 校验用户名是否已经注册过
        user = User.objects.filter(username=username)
        # 如果user存在，说明该用户名已注册
        if user:
            raise forms.ValidationError({'username': '用户名已存在'})
        # 如果密码和确认密码不一致，提示密码错误
        if userpwd != reuserpwd:
            raise forms.ValidationError({'reuserpwd': '两次密码不一致'})

        return self.cleaned_data


class UserIdentifyForm(forms.Form):
    """
    用户注册验证表单
    """
    realname = forms.CharField(required=True, max_length=20,
                               error_messages={'required': '姓名必填',
                                               'max_length': '姓名名不能超过20个字符', })
    identity = forms.CharField(required=True, min_length=6, max_length=20,
                               error_messages={'required': '身份证号必填必填',
                                               'max_length': '密码长度不能超过20字符',
                                               'min_length': '密码长度不能短于5个字符'})
    address = forms.CharField(required=True, max_length=255,
                              error_messages={'required': '地址必填'})

    phone = forms.CharField(required=True, max_length=11,
                            error_messages={'required': '电话号码必填', 'max_length': '电话号码长度不能超过11位'})

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if re.fullmatch(r'^1[34578]\d{9}$', phone):
            return phone
        else:
            raise forms.ValidationError('手机号码格式有误')
