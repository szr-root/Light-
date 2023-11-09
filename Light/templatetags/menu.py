import json
import copy
from django.http import QueryDict
from django.template import Library
# from django.conf import settings
from TB_test import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

register = Library()


@register.inclusion_tag("tag/menu.html")
def light_menu(request):
    current_url = request.path_info

    # 读取配置文件中的菜单的配置
    menu_list = copy.deepcopy(settings.Light_MENUS[request.light_user.is_admin])
    for item in menu_list:
        # item['class'] = "hide"
        for child in item['children']:
            if child['url'] == current_url:
                child['class'] = "active"
                # item['class'] = ""

    # print(menu_list)
    # print(json.dumps(menu_list, indent=2))
    return {"menu_list": menu_list}
