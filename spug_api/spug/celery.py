# -*- coding: utf-8 -*-
import os
from celery import Celery,platforms
from django.conf import settings

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spug.settings')

# 注册Celery的APP
app = Celery('spug')
# 绑定配置文件
# 'django.conf:settings'表示django,conf.settings也就是django项目的配置，celery会根据前面设置的环境变量自动查找并导入
# - namespace表示在settings.py中celery配置项的名字的统一前缀，这里是'CELERY_'，配置项的名字也需要大写
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现各个app下的tasks.py文件
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True