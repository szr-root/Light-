# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/04
# @File : adduser.py

# 启动django
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TB_test.settings')
django.setup()  # 伪造让django启动

from Light import models
from utils.encrypt import md5_string

models.Tester.objects.create(username='songzhaorui', password=md5_string("12345"), mobile="17780694752")
# models.Developer.objects.create(username='wangrui', password=md5_string("12345"), mobile="17780694753")
