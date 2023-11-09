from django.db import models


# Create your models here.

class ActiveBaseModel(models.Model):
    """ 激活状态 """
    active = models.SmallIntegerField(verbose_name='账号状态', default=1, choices=((1, '激活'), (2, '删除')))

    class Meta:
        abstract = True


# class Administrator(ActiveBaseModel):
#     """ 管理员表 """
#     username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)
#     password = models.CharField(verbose_name='密码', max_length=64)
#     mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
#     create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Tester(ActiveBaseModel):
    """ 其他测试人员表 """
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)
    password = models.CharField(verbose_name='密码', max_length=64, default='12345')
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    is_admin = models.SmallIntegerField(verbose_name='是否具有管理员权限', default=0,
                                        choices=[(0, '不具有'), (1, '具有')])
    name = models.CharField(verbose_name='姓名', max_length=32, db_index=True)
    create_date = models.DateTimeField(verbose_name='入职时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Developer(ActiveBaseModel):
    """ 开发表 """
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)
    password = models.CharField(verbose_name='密码', max_length=64, default='12345')
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True)
    is_admin = models.SmallIntegerField(verbose_name='是否具有管理员权限', default=0,
                                        choices=((0, '不具有'), (1, '具有')))

    name = models.CharField(verbose_name='姓名', max_length=32, db_index=True)
    create_date = models.DateTimeField(verbose_name='入职时间', auto_now_add=True)

    def __str__(self):
        return self.name


class Task(ActiveBaseModel):
    task_name = models.CharField(verbose_name='测试任务名', max_length=64)
    """ 测试任务表 """
    status_choices = (
        (1, "待启动"),
        (2, "测试中"),
        (3, "已完成测试"),
        (4, "测试暂停"),
    )
    status = models.SmallIntegerField(verbose_name="测试状态", choices=status_choices, default=1)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    start_datetime = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    finish_datetime = models.DateTimeField(verbose_name="完成时间", null=True, blank=True)
    oid = models.CharField(verbose_name="测试单号", max_length=64, unique=True)
    tester = models.ForeignKey(verbose_name="测试人员", to="Tester", on_delete=models.CASCADE)
    # tester = models.ManyToManyField(Tester)
    developer = models.ForeignKey(verbose_name='开发人员', to='Developer', on_delete=models.CASCADE)
    memo = models.TextField(verbose_name="备注", null=True, blank=True)


class TestRecord(ActiveBaseModel):
    """ 测试记录 """
    task_type_class_mapping = {
        1: "success",
        2: "danger",
        3: "default",
        4: "info",
        5: "primary",
    }
    task_type_choices = ((1, "测试完成"), (2, "不需要测试"), (3, "待启动"), (4, "测试阻塞"), (5, "测试中"),)
    charge_type = models.SmallIntegerField(verbose_name="类型", choices=task_type_choices)
    tester = models.ForeignKey(verbose_name="测试员", to="Tester", on_delete=models.CASCADE)
    developer = models.ForeignKey(verbose_name='开发人员', to='Developer', on_delete=models.CASCADE)
    creator = models.ForeignKey(verbose_name="创建者", to="Tester",
                                on_delete=models.CASCADE, null=True, blank=True, related_name='creater')
    order_oid = models.CharField(verbose_name="测试单号", max_length=64, null=True, blank=True, db_index=True)
    create_datetime = models.DateTimeField(verbose_name="任务创建时间", auto_now_add=True)
    start_time = models.DateTimeField(verbose_name="任务开始时间", auto_now_add=True)
    finish_time = models.DateTimeField(verbose_name="任务完成时间", auto_now_add=True)
    memo = models.TextField(verbose_name="备注", null=True, blank=True)
