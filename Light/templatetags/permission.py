from django.http import QueryDict
from django.template import Library
# from django.conf import settings
from Light.views.task.task import send_feishu_sheet
from TB_test import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()


@register.inclusion_tag("tag/breadcrumb.html")
def light_breadcrumb(request):
    permission_dict = settings.Light_PERMISSIONS[request.light_user.is_admin]
    url_name = request.resolver_match.url_name
    text_list = []
    current_dict = permission_dict.get(url_name)
    text_list.insert(0, {"text": current_dict['text'], "name": url_name})
    parent = current_dict['parent']
    while parent:
        loop = permission_dict[parent]
        # text_list.insert(0, loop['text'])
        text_list.insert(0, {"text": loop['text'], "name": parent})
        parent = loop['parent']

    text_list.insert(0, {"text": "首页", "name": "home"})
    return {'text_list': text_list}


@register.filter
def has_permission(request, name):
    # print(request, name)

    # 获取当前用户所有的权限
    permission_dict = settings.Light_PERMISSIONS[request.light_user.is_admin]

    # 是否有权限
    if name in permission_dict:
        return True
    return False


@register.simple_tag()
def gen_and_permission(request, name, title, *args, **kwargs):
    # 1.校验是否有权限
    permission_dict = settings.Light_PERMISSIONS[request.light_user.is_admin]
    if name not in permission_dict:
        return ""

    # 2.生成HTML链接
    url = reverse(name, args=args, kwargs=kwargs)
    html = f'<a href="{url}">{title}</a>'

    return mark_safe(html)
