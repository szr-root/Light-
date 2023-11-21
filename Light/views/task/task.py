# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/06
# @File : task.py

import time
import random
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect

from Light import models
from Light.views.account import get_referer_path
from utils.pager import Pagination
from Light.scripts.feishu import feishu_send_massage
from Light.forms.task import AddTask, TaskEditModelForm


def add_task(request):
    # 创建测试任务
    if request.method == 'GET':
        form = AddTask()
        return render(request, 'task/add_task.html', {'form': form})

    form = AddTask(data=request.POST)
    # print(request.POST)
    if not form.is_valid():
        return render(request, "task/add_task.html", {"form": form})

    while True:
        ctime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        rand_number = random.randint(10000000, 99999999)
        oid = f"{ctime}{rand_number}"
        exists = models.Task.objects.filter(oid=oid).exists()
        if not exists:
            break

    form.instance.oid = oid
    form.save()

    from django.contrib import messages
    messages.add_message(request, messages.SUCCESS, "新建任务成功")

    return redirect('all_task_list')


def my_task_list(request):
    if request.method == 'GET':
        queryset = models.Task.objects.filter(active=1, tester=request.light_user.id).order_by("-id")
        pager = Pagination(request, queryset)

        context = {'pager': pager}
        return render(request, 'task/task_list.html', context)


def all_task_list(request):
    if request.method == 'GET':
        queryset = models.Task.objects.filter(active=1).order_by("-id")
        pager = Pagination(request, queryset)

        context = {'pager': pager}
        return render(request, 'task/task_list.html', context)


def edit_task(request, pk):
    instance = models.Task.objects.filter(id=pk, active=1).first()
    if request.method == 'GET':
        referer_path = get_referer_path(request)
        # print(referer_path)
        if referer_path == '/task/my_task_list/':
            print('my!!!!!')
            source = '0'
        else:
            print('all!!!!!')
            source = '1'

        # if request.method == "GET":
        form = TaskEditModelForm(instance=instance)
        return render(request, "task/edit_task.html", {"form": form, 'source': source})

    form = TaskEditModelForm(data=request.POST, instance=instance)

    if not form.is_valid():
        return render(request, "task/edit_task.html", {"form": form})
    # source = form.cleaned_data.pop('source')
    form.save()
    source = request.POST['source']
    # print(source)
    if source == '1':
        return redirect('/task/all_task_list/')
    else:
        return redirect('/task/my_task_list/')


def delete_task(request, pk):
    origin = request.GET.get("redirect", "task/task_list")
    if request.method == "GET":
        return render(request, "delete.html", {"origin": origin})

    models.Task.objects.filter(id=pk, active=1).update(active=0)
    return redirect(origin)


def task_together(request):
    objects = models.Task.objects.filter(active=1).all()
    messages = ''
    finish = []
    doing = []
    stop = []
    for object in objects:
        # 已完成
        task_name = object.task_name
        memo = object.memo
        tester_queryset = object.tester.all()
        testers = []
        for tester in tester_queryset:
            testers.append(tester.name)
        testers_str = ','.join(testers)
        task_status = object.get_status_display()
        finish_datetime = object.finish_datetime
        if finish_datetime is not None:
            if task_status == '已完成测试' and finish_datetime.strftime("%Y%m%d") == datetime.date.today().strftime(
                    "%Y%m%d"):
                finish.append(f'{task_name} ,{task_status}, {memo} --- {testers_str}\n')
        if task_status == '测试中':
            doing.append(f'{task_name} ,{task_status}, {memo} --- {testers_str}\n')
        if task_status == '待启动' or task_status == '测试暂停':
            stop.append(f'{task_name} ,{task_status}, {memo} \n')

    # print(finish, doing, stop)
    if len(finish) != 0:
        messages += '已完成:\n'
        i = 1
        for item in finish:
            messages += f'{i}. {item}'
            i += 1
    if len(doing) != 0:
        messages += '\n进行中:\n'
        i = 1
        for item in doing:
            messages += f'{i}. {item}'
            i += 1
    if len(stop) != 0:
        messages += '\n暂停:\n'
        i = 1
        for item in stop:
            messages += f'{i}. {item}'
            i += 1

    return render(request, 'task/task_together.html', {'messages': messages})


def send_feishu(request):
    objects = models.Task.objects.filter(active=1).all()
    messages = ''
    finish = []
    doing = []
    stop = []
    for object in objects:
        # 已完成
        task_name = object.task_name
        memo = object.memo
        tester = object.tester
        task_status = object.get_status_display()
        finish_datetime = object.finish_datetime
        if finish_datetime is not None:
            if task_status == '已完成测试' and finish_datetime.strftime("%Y%m%d") == datetime.date.today().strftime(
                    "%Y%m%d"):
                finish.append(f'{task_name} ,{task_status}, {memo} --- {tester}\n')
        if task_status == '测试中':
            doing.append(f'{task_name} ,{task_status}, {memo} --- {tester}\n')
        if task_status == '待启动' or task_status == '测试暂停':
            stop.append(f'{task_name} ,{task_status}, {memo} --- {tester}\n')

    # print(finish, doing, stop)
    if len(finish) is not None:
        messages += '已完成:\n'
        i = 1
        for item in finish:
            messages += f'{i}. {item}'
            i += 1

    if len(doing) is not None:
        messages += '\n进行中:\n'
        i = 1
        for item in doing:
            messages += f'{i}. {item}'
            i += 1
    if len(stop) is not None:
        messages += '\n暂停:\n'
        i = 1
        for item in stop:
            messages += f'{i}. {item}'
            i += 1

    feishu_send_massage(messages)
    return redirect('task_together')
