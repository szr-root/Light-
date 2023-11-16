# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/04
# @File : account.py

from django import forms

from Light import models
from utils.bootstrap import BootStrapForm
from utils.encrypt import md5_string


class LoginForm(BootStrapForm, forms.Form):
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("0", "开发"), ("1", "测试"),)
    )

    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        old = self.cleaned_data['password']
        return md5_string(old)


class AddDevelop(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['is_admin', 'create_date']
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("0", "开发"), ("1", "测试"),)
    )

    class Meta:
        model = models.Developer
        fields = ['role', 'username', 'password', 'name', 'mobile', 'is_admin']
        widgets = {
            "role": forms.RadioSelect(attrs={'class': "form-radio"}),
            'password': forms.TextInput(attrs={'help_text': '默认12345'}),
            "is_admin": forms.RadioSelect(attrs={'class': "form-radio"})
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5_string(password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EditDevelop(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['is_admin', 'create_date']

    class Meta:
        model = models.Developer
        fields = ['username', 'password', 'name', 'mobile', 'is_admin']
        widgets = {
            # 'password': forms.PasswordInput(attrs={'help_text': '默认12345'}),
            "is_admin": forms.RadioSelect(attrs={'class': "form-radio"})
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5_string(password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AddTester(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['is_admin', 'create_date']
    role = forms.ChoiceField(
        label="角色",
        required=True,
        choices=(("0", "开发"), ("1", "测试"),)
    )

    class Meta:
        model = models.Tester
        fields = ['role', 'username', 'password', 'name', 'mobile', 'is_admin']
        widgets = {
            "role": forms.RadioSelect(attrs={'class': "form-radio"}),
            'password': forms.TextInput(attrs={'help_text': '默认12345'}),
            "is_admin": forms.RadioSelect(attrs={'class': "form-radio"})
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5_string(password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
