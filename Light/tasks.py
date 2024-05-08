# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2024/04/24
# @File : tasks.py

from celery import shared_task


@shared_task
def add(a, b=20):
    return a + b

