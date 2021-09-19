# -*- coding: utf-8 -*-

from spug.celery import app
from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import RancherNamespace,RancherConfigMap

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
        url = settings.RANCHER_CONFIGMAP.format(xx["namespace_id"])
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