# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/11/06
# @File : task.py


from django import forms

from Light import models
from utils.bootstrap import BootStrapForm


class AddTask(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['tester', 'developer', 'status', 'create_datetime', 'oid', 'finish_datetime', ]

    tester = forms.ModelMultipleChoiceField(label="参与的测试人员", queryset=models.Tester.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline'}))
    developer = forms.ModelMultipleChoiceField(label="参与的开发人员", queryset=models.Developer.objects.all(),
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'form-check-inline'}))

    class Meta:
        model = models.Task
        fields = ['task_name', 'start_datetime', 'tester', 'developer', 'memo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TaskEditModelForm(BootStrapForm, forms.ModelForm):
    exclude_field_list = ['tester', 'developer','status', 'create_datetime', 'oid']
    # source = forms.ChoiceField(
    #     label="来源",
    #     choices=(("0", "开发"), ("1", "测试"),)
    # )
    tester = forms.ModelMultipleChoiceField(label="参与的测试人员", queryset=models.Tester.objects.filter(active=1).all(),
                                            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-inline custom-checkbox'}))
    developer = forms.ModelMultipleChoiceField(label="参与的开发人员", queryset=models.Developer.objects.filter(active=1).all(),
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'form-check-inline'}))

    class Meta:
        status_choices = (
            (1, "待启动"),
            (2, "测试中"),
            (3, "已完成测试"),
            (4, "测试阻塞"),
            (5, "不需要测试"),
        )
        model = models.Task
        fields = ['task_name', 'status', 'start_datetime', 'finish_datetime', 'tester', 'developer', 'memo']
        widgets = {
            # forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': 'form-control'}))
            'status': forms.Select(attrs={'class': 'btn btn-info dropdown-toggle'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
