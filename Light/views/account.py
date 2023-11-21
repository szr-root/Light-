# from django.conf import settings

import os
from urllib.parse import urlparse

from TB_test import settings
from django.urls import resolve
from django.shortcuts import render, redirect, HttpResponse
from Light.forms.account import LoginForm, AddUser, AddTester
from Light import models
from utils.encrypt import md5_string


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    # print(request.POST)
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {'form': form})
    data_dict = form.cleaned_data
    # print(data_dict)
    role = data_dict.pop('role')
    # 取数据库查询
    if role == '1':
        user_object = models.Tester.objects.filter(**data_dict).filter(active=1).first()
    else:
        user_object = models.Developer.objects.filter(**data_dict).filter(active=1).first()
    # 如果没有数据
    if not user_object:
        form.add_error('password', '用户名或密码错误')
        return render(request, "login.html", {"form": form})

    # 是否具备管理员权限
    # is_admin = data_dict.pop('is_admin')
    is_admin = user_object.is_admin

    # print(is_admin)

    # 数据存在就保存session
    mapping_role = {'0': '开发', '1': '测试'}
    mappin_admin = {'0': 'Normal', '1': 'Admin'}

    request.session[settings.Light_SESSION_KEY] = {
        "role": mapping_role[role],
        "id": user_object.id,
        "name": user_object.name,
        "is_admin": mappin_admin[str(is_admin)]
    }

    # 登录成功，跳转后台
    return redirect(settings.HOME_URL)


def logout(request):
    request.session.clear()
    return redirect("login")


def get_referer_path(request):
    referer = request.META.get('HTTP_REFERER', None)

    if referer:
        parsed_url = urlparse(referer)
        # 获取路径部分
        referer_path = parsed_url.path
        return referer_path

    return None


def add_user(request):

    # if referer_path:
    #     list = referer_path.split('/')[2]
    # else:
    #     list = settings.HOME_URL
    # print(list)
    if request.method == 'GET':
        referer_path = get_referer_path(request)
        # print(referer_path)
        if referer_path == '/user/tester_list/':
            print('test!!!!!')
            form = AddUser(initial={'role': '1'})
        else:
            print('deve!!!!!')
            form = AddUser(initial={'role': '0'})
        # request.session['rul'] = referer_path
        return render(request, "add_user.html", {'form': form})

    role = request.POST['role']
    if role == '1':
        form = AddTester(data=request.POST)
        msg = '新建测试人员成功'
    else:
        form = AddUser(data=request.POST)
        msg = '新建开发人员成功'

    if not form.is_valid():
        return render(request, "add_user.html", {'form': form})

    role = form.cleaned_data.pop('role')


    pwd = form.cleaned_data['password']
    form.cleaned_data['password'] = md5_string(pwd)

    # print(form.cleaned_data)
    form.save()

    from django.contrib import messages
    messages.add_message(request, messages.SUCCESS, msg)
    # print(role)
    if role:
        return redirect('/user/develop_list/')
    else:
        return redirect('/user/tester_list/')


def home(request):
    return render(request, 'home.html')

    # def sms_login(request):
    #     # 1.GET请求看到登录页面
    #     if request.method == "GET":
    #         form = SmsLoginForm()
    #         return render(request, "sms_login.html", {"form": form})
    #
    #     print(request.META)
    #     # 2.格式校验（手机号+验证码）
    #     # 3.验证码是否正确？手机号去redis中校验
    #     form = SmsLoginForm(request.POST)
    #     if not form.is_valid():
    #         return JsonResponse({"status": False, "msg": form.errors})
    #
    #     # 4.去数据库中读取用户信息 + 保存Session
    #     role = form.cleaned_data['role']
    #     mobile = form.cleaned_data['mobile']
    #     if role == "1":
    #         user_object = models.Administrator.objects.filter(mobile=mobile).filter(active=1).first()
    #     else:
    #         user_object = models.Customer.objects.filter(mobile=mobile).filter(active=1).first()
    #
    #     # 5.数据不存在
    #     if not user_object:
    #         return JsonResponse({"status": False, "msg": {"mobile": ["手机号不存在"]}})
    #
    #     # 2.4 数据存在，将用户信息存储session
    #     mapping = {"1": "ADMIN", "2": "CUSTOMER"}
    #     request.session[settings.NB_SESSION_KEY] = {
    #         "role": mapping[role],  # "ADMIN"  "CUSTOMER"
    #         "id": user_object.id,
    #         "name": user_object.username,
    #     }
    #     return JsonResponse({"status": True, "msg": "OK", "data": settings.HOME_URL})
    #
    #
    # @csrf_exempt
    # def send_sms(request):
    #     """ 发送短信"""
    #     # 1.校验手机格式是否正确（是否已经注册？）
    #     # 2.校验手机号发送频率（第三方短信平台）
    #     # 3.生成短信验证码 + 发送
    #     form = SendSmsForm(data=request.POST)
    #     if not form.is_valid():
    #         return JsonResponse({"status": False, "msg": form.errors})
    #
    #     return JsonResponse({"status": True, "msg": "OK"})
    #
    #
    # def home(request):
    #     return render(request, "home.html")
    #
    #
    # def user(request):
    #     # return HttpResponse("USER")
    #     return render(request, "user.html")
    #
    #
    # def add_user(request):
    #     # return HttpResponse("USER")
    #     return render(request, "add_user.html")
    #
    #
    # def multi_import(request):
    #     # return HttpResponse("multi_import")
    #     return render(request, "multi_import.html")
    #
    #
    # def edit_user(request, uid):
    #     return HttpResponse("edit_user")
