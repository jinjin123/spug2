# -*- coding: utf-8 -*-

from celery import shared_task

# 自定义要执行的task任务
@shared_task()
def print_hello():
    return 'hello celery and django...'

@shared_task()
def test():
    pass