# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/06
# @File : info.py

from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from Light import models
from utils.encrypt import md5_string
from utils.bootstrap import BootStrapForm
from utils.pager import Pagination


class ResetPasswordModelForm(BootStrapForm, forms.ModelForm):
    confirm_password = forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Tester
        fields = ['password', 'confirm_password', ]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5_string(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5_string(self.cleaned_data.get('confirm_password', ''))

        if password != confirm_password:
            raise ValidationError("两次密码不一致")
        return confirm_password


def info_list(request):
    # 获取当前用户信息
    instance = models.Tester.objects.filter(id=request.light_user.id, active=1).first()
    if request.method == "GET":
        # 生成Form表单
        form = ResetPasswordModelForm()
        context = {"instance": instance, 'form': form}
        return render(request, 'user/info_list.html', context)

    form = ResetPasswordModelForm(instance=instance, data=request.POST)
    if not form.is_valid():
        context = {"instance": instance, 'form': form}
        return render(request, 'user/info_list.html', context)

    form.save()
    messages.add_message(request, messages.SUCCESS, "重置密码成功")
    return redirect("info_list")

    # form.save()
    # context = {
    #     "instance": instance,
    #     'form': ResetPasswordModelForm(),
    #     "success": "修改成功"
    # }
    # return render(request, 'user/info_list.html', context)


def develop_list(request):
    queryset = models.Developer.objects.filter(active=1).all()
    pager = Pagination(request, queryset)
    context = {'pager': pager}
    return render(request, 'user/user_list.html', context)


def tester_list(request):
    queryset = models.Tester.objects.filter(active=1).all()
    pager = Pagination(request, queryset)
    context = {'pager': pager}
    return render(request, 'user/user_list.html', context)
