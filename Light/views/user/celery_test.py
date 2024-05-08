# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2024/04/24
# @File : celery_test.py
from time import sleep

from django.http import JsonResponse

from Light.tasks import add

from django.shortcuts import HttpResponse


def get_mobie(request):
    mobile = int(request.GET.get('mobile'))
    print(mobile)
    res = add.delay(mobile, 5)

    return JsonResponse({'code': 200, 'msg': res.id})
