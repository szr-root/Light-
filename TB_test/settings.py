"""
Django settings for TB_test project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c$7@07^_qc11%%miq=oo820dj#1l8hg=f$e*_r_8=-77*ef&7$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Light.apps.LightConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "utils.md.AuthMiddlewarePathInfo",
    "utils.md.PermissionMiddleware",
]

ROOT_URLCONF = 'TB_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TB_test.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Light',  # 数据库名字
        'USER': 'root',
        'PASSWORD': 'songzhaoruizx',
        'HOST': '127.0.0.1',  # ip
        'PORT': 3306,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "qwe123",
            # 'MAX_ENTRIES': 300,  # 最大缓存个数（默认300）
            # 'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

USE_I18N = True

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

############
# 项目配置   #
############
HOME_URL = "/home/"
Light_SESSION_KEY = "user_info"
Light_LOGIN_NAME = "login"

############
# SESSIONS #
############
# Session存储在哪里？
# SESSION_ENGINE = "django.contrib.sessions.backends.db"

# 如果存储到文件中，文件的路径。
# SESSION_ENGINE = "django.contrib.sessions.backends.file"
# SESSION_FILE_PATH = None

# 存储到缓存
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

Light_WHITE_URL = ["/login/", "/sms/login/", '/send/sms/', 'add_new_develop/']
Light_WHITE_PERMISSION_NAME = ["login", "sms_login", "send_sms", ]
# NB_PERMISSIONS = {
#     "ADMIN": ["home", ],
#     "CUSTOMER": ['home', 'user'],
# }
#
Light_PERMISSIONS = {
    "Admin": {
        "logout": {"parent": None, "text": "退出"},
        "home": {"parent": None, "text": "个人中心"},
        "add_user": {"parent": None, "text": "添加用户"},
        "info_list": {"parent": None, "text": "个人资料"},

        'task_list': {"parent": None, "text": "任务记录"},
        'add_task': {"parent": 'task_list', "text": "创建任务"},
        'edit_task': {"parent": 'task_list', "text": "编辑任务"},
        'delete_task': {"parent": 'task_list', "text": "编辑任务"},
        'send_feishu': {"parent": 'task_list', "text": "编辑任务"},

        'anchor_online': {"parent": None, "text": "主播上线"},

        'develop_list':{"parent": None, "text": "测试人员"},
    },
    "Normal": {
        "logout": {"parent": None, "text": "退出"},
        "home": {"parent": None, "text": "个人中心"},
        # "add_new_develop": {"parent": None, "text": "添加用户"},

        'task_list': {"parent": None, "text": "任务记录"},
        'add_task': {"parent": 'task_list', "text": "创建任务"},
        'edit_task': {"parent": 'task_list', "text": "编辑任务"},
        'delete_task': {"parent": 'task_list', "text": "编辑任务"},
        'send_feishu': {"parent": 'task_list', "text": "编辑任务"},

        'anchor_online': {"parent": None, "text": "主播上线"},

    },
}

Light_MENUS = {
    "Admin": [
        {
            "text": "用户信息",
            'icon': "fa-bed",
            "children": [
                {"text": "个人资料", "name": "info", "url": "/info/list/"},
                {"text": "添加用户", "name": "add_user", "url": "/add_user/"},

            ]
        },
        {
            "text": "测试记录",
            'icon': "fa-bed",
            "children": [
                {"text": "我的测试任务", "name": "task_lst", "url": "/task/task_list"},
                {"text": "创建测试任务", "name": "add_task", "url": "/task/add_task"},
            ]
        },
        {"text": "测试工具",
         'icon': "fa-bed",
         "children": [
             {"text": "批量上线一些主播", "name": "anchor_online", "url": "anchor_online"},
         ]
         },

        {"text": "人员组成",
         'icon': "fa-bed",
         "children": [
             {"text": "开发人员", "name": "develop_list", "url": "user/develop_list"},
             {"text": "测试人员", "name": "tester_list", "url": "user/tester_list"},

         ]
         },
    ],
    "Normal": [
        {
            "text": "用户信息",
            'icon': "fa-bed",
            "children": [
                {"text": "个人资料", "name": "info", "url": "/info/list/"},
                # {"text": "添加用户", "name": "add_new_develop", "url": "/add_new_develop/"},

            ]
        },
        {
            "text": "测试记录",
            'icon': "fa-bed",
            "children": [
                {"text": "我的测试任务", "name": "task_lst", "url": "/task/task_list"},
                {"text": "创建测试任务", "name": "add_task", "url": "/task/add_task"},
            ]
        },
        {"text": "测试工具",
         'icon': "fa-bed",
         "children": [
             {"text": "批量上线一些主播", "name": "anchor_online", "url": "anchor_online"},
         ]
         },
    ]
}

#
# try:
#     # 放到最后，是为了将前面的覆盖吗
#     from .local_settings import *
# except ImportError:
#     pass
