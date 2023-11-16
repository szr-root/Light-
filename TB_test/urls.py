"""
URL configuration for TB_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Light.views import account
from Light.views.user import info
from Light.views.task import task
from Light.views.work import anchor

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 用户相关
    path('login/', account.login, name='login'),
    path('home/', account.home, name='home'),
    path('logout/', account.logout, name='logout'),
    path('add_user/', account.add_user, name='add_user'),
    path('info/list/', info.info_list, name='info_list'),

    # 测试任务相关
    path('task/my_task_list/', task.my_task_list, name='my_task_list'),
    path('task/all_task_list/', task.all_task_list, name='all_task_list'),
    path('task/add_task/', task.add_task, name='add_task'),
    path('task/edit_task/<int:pk>/', task.edit_task, name='edit_task'),
    path('task/delete_task/<int:pk>/', task.delete_task, name='delete_task'),
    path('task/task_together/', task.task_together, name='task_together'),
    path('task/send_feishu/', task.send_feishu, name='send_feishu'),

    # 业务相关
    path('anchor/anchor_online/', anchor.anchor_online, name='anchor_online'),

    # 人员相关
    path('user/develop_list/', info.develop_list, name='develop_list'),
    path('user/edit_develop/<int:pk>/', info.edit_develop, name='edit_develop'),
    path('user/delete_develop/<int:pk>/', info.delete_develop, name='delete_develop'),
    path('user/tester_list/', info.tester_list, name='tester_list'),
    path('user/edit_tester/<int:pk>/', info.edit_tester, name='edit_tester'),
    path('user/delete_tester/<int:pk>/', info.delete_tester, name='delete_tester'),

]
