# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/06
# @File : task.py


from django import forms

from Light import models
from utils.bootstrap import BootStrapForm


class AddTask(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['status', 'create_datetime', 'oid', 'finish_datetime', ]

    class Meta:
        model = models.Task
        fields = ['task_name', 'start_datetime', 'tester', 'developer', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TaskEditModelForm(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['status', 'create_datetime', 'oid' ]

    class Meta:
        status_choices = (
            (1, "待启动"),
            (2, "测试中"),
            (3, "已完成测试"),
            (4, "测试阻塞"),
            (5, "不需要测试"),
        )
        model = models.Task
        fields = ['task_name', 'status', 'start_datetime','finish_datetime', 'tester', 'developer', 'memo']
        widgets = {
            # forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}))
            'status': forms.Select(attrs={'class': 'btn btn-info dropdown-toggle'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
