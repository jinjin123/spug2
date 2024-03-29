# -*- coding: utf-8 -*-

from spug.celery import app
from libs.utils import RequestApiAgent
from django.conf import settings
from django.db.models import Q
import json
from apps.app.models import *
from apps.config.models import RancherApiConfig
from django.core.mail import send_mail
from apps.schedule.models import Task
from apps.message.models import EmailRecord
import logging
from django.core.cache import cache
import socket
logger = logging.getLogger('spug_info')

@app.task
def get_namespace():
    url = settings.RANCHER_DEV_NS_URL
    token = settings.RANCHER_DEV_TOKEN
    kwargs = {
        "url": url,
        "headers": {"Authorization": token, "Content-Type": "application/json"}
    }
    try:
        res = RequestApiAgent().list(**kwargs)
        datalist = (json.loads(res.content))["data"]
        namespace_bulk = []
        for x in datalist:
            if x["name"] != "kube-system" and x["name"] != "kube-public" and x["name"] != "kube-node-lease" and x["projectId"] != "local:p-zsr86":
                namespace_bulk.append(RancherNamespace(
                    namespace=x["name"],
                    namespace_id=x["projectId"]
                ))
        RancherNamespace.objects.bulk_create(namespace_bulk)
    except Exception as e:
        return "Error:{}".format(e)

@app.task
def get_configMap():
    ns = RancherNamespace.objects.all().values("namespace_id")
    for xx in ns:
        url = settings.RANCHER_DEV_CONFIGMAP.format(xx["namespace_id"])
        token = settings.RANCHER_DEV_TOKEN
        kwargs = {
            "url": url,
            "headers": {"Authorization": token, "Content-Type": "application/json"}
        }
        try:
            res = RequestApiAgent().list(**kwargs)
            datalist = (json.loads(res.content))["data"]
            config_bulk = []
            global x
            for x in datalist:
                # print(x["name"])
                if x.get("data", None):
                    for k, v in dict.items(x["data"]):
                        config_bulk.append(
                            RancherConfigMap(
                                namespace=RancherNamespace.objects.filter(namespace_id=x["projectId"]).first(),
                                configid=x["id"],
                                configname=x["name"],
                                configMap_k=k,
                                configMap_v=v
                            )
                        )
                # print(type(x["data"]))
            RancherConfigMap.objects.bulk_create(config_bulk)
        except Exception as e:
            return "Body:{}\nError:{}".format(x,e)


@app.task
def send_mail_task(subject,content,from_mail,to_email):
    """发送邮件"""
    # if not isinstance(message_obj, EmailRecord):
    #     msg = 'send_mail_task_error:message_obj is not EmailRecord obj'
    #     logger.error(msg)
    #     return msg
    try:
        r = send_mail(subject, content, from_mail,
                      [to_email], fail_silently=False)
        if r > 0:
            message = EmailRecord.objects.create(
                to_email=to_email,
                from_email=from_mail,
                subject=subject,
                content=content,
            )
            message.is_pushed = True
            message.save()
    except:
        logger.error('send_mail_task_error', exc_info=True)

@app.task
def check_svc_status():
    try:
        t = ProjectService.objects.filter(~Q(state="active")).values("id","statuslinks")
        for x in t:
            if x["statuslinks"] is not None and (x["statuslinks"]).find("ioc.com") > -1:
                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC", tag="ioc").first()
                kwargs = {
                    "url":  x["statuslinks"],
                    "headers": {"Authorization": Action.token, "Content-Type": "application/json"},
                }
                res = RequestApiAgent().list(**kwargs)
                red = json.loads(res.content)
                if res.status_code != 200:
                    logger.error(msg="request rancher svc api status code !200 ")
                ProjectService.objects.filter(id=x["id"]).update(state=red['state'])
            else:
                if x["statuslinks"] is not None and (x["statuslinks"]).find("feiyan.com") > -1:
                    Action = RancherApiConfig.objects.filter(env_id=3, label="GETSVC",tag="feiyan").first()
                    kwargs = {
                        "url": x["statuslinks"],
                        "headers": {"Authorization": Action.token, "Content-Type": "application/json"},
                    }
                    res = RequestApiAgent().list(**kwargs)
                    red = json.loads(res.content)
                    if res.status_code != 200:
                        logger.error(msg="request rancher svc api status code !200 ")
                    ProjectService.objects.filter(id=x["id"]).update(state=red['state'])

    except Exception as e:
        logger.error('########get svcdata fail #######--->', e)


@app.task
def clearmaster():
    m = cache.get("tmpmaster", [])
    if len(m) > 0:
        logger.info(msg='######## del master start #######--->')
        for x in m:
            User.objects.filter(id=x).update(role_id=2)
        logger.info(msg='######## del master done #######--->')


@app.task
def patch_task():
    kwargs = {
        "url": "",
        "headers": {"X-Token": User.objects.get(id=1).access_token, "Content-Type": "application/json","x-forwarded-for":"19.104.50.128","x-real-ip":"19.104.50.128"},
    }
    try:
        for task in Task.objects.filter(is_active=False):
            kwargs['url'] = "http://19.104.50.128:8011/api/schedule/"
            kwargs['data'] = json.dumps({"id": task.id, "is_active": True})
            logger.info(msg='#### patch job  start ####')
            res = RequestApiAgent().patch(**kwargs)
            logger.info(msg='### contnet '+str(json.loads(res.content)))
            logger.info(msg='#### patch job  done ####')
    except Exception as e:
        logger.error(msg="patch job update error->"+ str(e))

@app.task
def updatetoken():
    try:
        kwargs = {
            "url": "",
            "headers": {"X-Token": User.objects.get(username='deploy').access_token, "Content-Type": "application/json","x-forwarded-for":"19.104.50.128","x-real-ip":"19.104.50.128"}
        }
        kwargs['url'] = "http://19.104.50.128:8011/api/account/login/"
        kwargs['data'] = json.dumps({"username":"deploy","password":"test123","type":"default"})
        logger.info(msg="update deploy status start")
        res = RequestApiAgent().create(**kwargs)
        logger.info(msg="update deploy status ->" + str(json.loads(res.content)))

    except Exception as e:
        logger.error(msg="update token error->"+ str(e))
