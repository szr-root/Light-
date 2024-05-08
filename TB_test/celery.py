# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2024/04/24
# @File : celery.py

import os
from celery import Celery

# 1 导入django的配置文件---》后续在celery的任务中，就可以直接使用django的orm，缓存。。。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TB_test.settings')
# 2 实例化得到celery对象
app = Celery('proj')
# 3 celery的配置，使用django 配置文件中的配置--》刚刚写的配置
app.config_from_object('django.conf:settings')

# 4 这句话会去所有app中，自动查找 tasks.py 文件，作为任务文件
app.autodiscover_tasks()

# 启动一个worker
# celery -A TB_test worker -l debug

# 启动定时任务
# celery -A TB_test beat -l debug

# celery监控 flower
# celery -A TB_test flower --port-5555
