# -*- coding: utf-8 -*-

from spug.celery import app
from celery import shared_task

# 自定义要执行的task任务
@app.task
def print_hello():
    return 'hello celery and django...'

@app.task
def test():
    pass