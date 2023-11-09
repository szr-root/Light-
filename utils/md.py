from django.utils.deprecation import MiddlewareMixin
# from django.conf import settings
from TB_test import settings
from django.shortcuts import redirect, HttpResponse, render
from django.http import JsonResponse


class Context:
    def __init__(self, role, id, name,is_admin):
        self.role = role
        self.id = id
        self.name = name
        self.is_admin = is_admin


class AuthMiddleware(MiddlewareMixin):

    def is_white_url_by_path_info(self, request):
        if request.path_info in ["/login/", "/sms/login/", '/send/sms/']:
            return True

    def is_white_url_by_name(self, request):
        url_name = request.resolver_match.url_name
        if url_name in ["login", "sms_login", "send_sms"]:
            return True

    def process_request(self, request):
        return

        # 0.白名单，有些无需登录就能访问的页面【login】【sms/login】【send/sms】
        # path('login/', account.login, name='login'),
        # path('sms/login/', account.sms_login, name='sms_login'),
        # path('send/sms/', account.send_sms, name='send_sms'),
        # if request.path_info in ["/login/", "/sms/login/", '/send/sms/']:
        #     return
        if self.is_white_url_by_path_info(request):
            return

        # 1.去session中读取用户信息
        # request.session["user_info"] = {
        #     "role": mapping[role],  # "ADMIN"  "CUSTOMER"
        #     "id": user_object.id,
        #     "name": user_object.username,
        # }
        data_dict = request.session.get(settings.NB_SESSION_KEY)

        # 2.不存在->未登录
        if not data_dict:
            # return redirect("/login/")
            return redirect(settings.Light_LOGIN_NAME)

        # 3.存在，则继续往后走
        request.light_user = Context(**data_dict)
        # print(request.nb_user.name)
        # print(request.nb_user.id)
        # print(request.nb_user.role)

    def process_view(self, request, callback, *args, **kwargs):

        # 0.白名单，有些无需登录就能访问的页面【login】【sms/login】【send/sms】
        # path('login/', account.login, name='login'),
        # path('sms/login/', account.sms_login, name='sms_login'),
        # path('send/sms/', account.send_sms, name='send_sms'),
        # url_name = request.resolver_match.url_name
        # if url_name in ["login", "sms_login", "send_sms"]:
        #     return
        if self.is_white_url_by_name(request):
            return
        # 1.去session中读取用户信息
        # request.session["user_info"] = {
        #     "role": mapping[role],  # "ADMIN"  "CUSTOMER"
        #     "id": user_object.id,
        #     "name": user_object.username,
        # }
        data_dict = request.session.get(settings.Light_SESSION_KEY)

        # 2.不存在->未登录
        if not data_dict:
            return redirect(settings.Light_LOGIN_NAME)

        # 3.存在，则继续往后走
        request.light_user = Context(**data_dict)
        print(Context)
        # print(request.nb_user.name)
        # print(request.nb_user.id)
        # print(request.nb_user.role)


class AuthMiddlewarePathInfo(MiddlewareMixin):

    def is_white_url_by_path_info(self, request):
        if request.path_info in settings.Light_WHITE_URL:
            return True

    def process_request(self, request):
        if self.is_white_url_by_path_info(request):
            return
        # 1.去session中读取用户信息
        data_dict = request.session.get(settings.Light_SESSION_KEY)

        # 2.不存在->未登录
        if not data_dict:
            return redirect(settings.Light_LOGIN_NAME)

        # 3.存在，则继续往后走
        request.light_user = Context(**data_dict)


class PermissionMiddleware(MiddlewareMixin):

    def is_white_name(self, request):
        url_name = request.resolver_match.url_name
        if url_name in settings.Light_WHITE_PERMISSION_NAME:
            return True

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def process_view(self, request, callback, *args, **kwargs):
        # 1.有些不需要做权限校验
        if self.is_white_name(request):
            return

        # 2.获取用户登录信息
        # role = request.light_user.role
        is_admin = request.light_user.is_admin

        # 3.获取当前用户所有的权限
        permission_dict = settings.Light_PERMISSIONS[is_admin]

        # 4.权限校验
        url_name = request.resolver_match.url_name
        if url_name in permission_dict:
            return

        # 5.无权限（是否是ajax请求）
        # X-Requested-With: XMLHttpRequest
        # request封装请求相关的所有数据 + 方法 method/path_info/resolver_match
        # return HttpResponse("无权访问")
        # return render(request, '404.html')
        if self.is_ajax(request):
            return JsonResponse({'status': False, 'msg': "无权访问"})
        return render(request, '404.html')
