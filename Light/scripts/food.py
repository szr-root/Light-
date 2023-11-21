# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/20
# @File : food.py

import random

# 假设你有一个列表
import time

my_list = ['英郡','C8','D区']

# 设置选择次数
num_selections = 100

# 使用字典来存储每个值被选中的次数
selection_counts = {}

for _ in range(num_selections):
    # 随机选择列表中的一个元素
    selected_value = random.choice(my_list)

    # 更新字典中对应值的计数
    if selected_value in selection_counts:
        selection_counts[selected_value] += 1
    else:
        selection_counts[selected_value] = 1

v = ''
num = 0
# 打印每个值被选中的次数
for value, count in selection_counts.items():
    print(f"{value}: {count}次")
    if count > num:
        v = value
        num = count

print(f'\n{time.strftime("%Y-%m-%d %H:%M:%S")}\n最终结果中午吃{v}')