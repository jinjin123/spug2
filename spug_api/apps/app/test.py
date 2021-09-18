from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import RancherNamespace,RancherConfigMap
import unittest


class Mytest(unittest.TestCase):
    def test_get_rancher(self):
        url = settings.RANCHER_DEV_URL
        token = settings.RANCHER_TOKEN
        kwargs = {
            "url": url,
            "headers": {"Authorization": token,"Content-Type": "application/json"}
        }
        try:
            res = RequestApiAgent().list(**kwargs)
            datalist = (json.loads(res.content))["data"]
            namespace_bulk = []
            for x in datalist:
                # print(x["name"])
                if x["name"] != "kube-system" and x["name"]  != "kube-public"  and x["name"]  != "kube-node-lease" and x["projectId"] != "local:p-zsr86":
                    namespace_bulk.append(RancherNamespace(
                        namespace=x["name"],
                        namespace_id=x["projectId"]
                        # env_id=1,
                        # create_by_id=1
                    ))
            # print(namespace_bulk)
            # RancherNamespace.objects.bulk_create(namespace_bulk)
            return res.status_code
        except Exception as e:
            print(e)
            return e

    def test_get_configmap(self):
        ns = RancherNamespace.objects.all().values("namespace_id")
        for xx in ns:
            # print(x["namespace_id"])
            url = settings.RANCHER_CONFIGMAP.format(xx["namespace_id"])
            token = settings.RANCHER_TOKEN
            kwargs = {
                "url": url,
                "headers": {"Authorization": token,"Content-Type": "application/json"}
            }
            # print(RancherNamespace.objects.filter(namespace_id=xx["namespace_id"])[:1])
            try:
                res = RequestApiAgent().list(**kwargs)
                datalist = (json.loads(res.content))["data"]
                config_bulk = []
                global x
                for x in datalist:
                    # print(x["name"])
                    if x.get("data",None):
                        for k,v in dict.items(x["data"]):
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
                print(x)
                print(e)
    def test(self):
        ns = RancherNamespace.objects.all().values("namespace_id")
        print(list(ns))
        conf = RancherConfigMap.objects.filter(id=381)
        print(list(conf)[0].configMap_v)
        tmp= []
        for x in conf:
            tmp.append({
                "id":x.id,
                "configid": x.configid,
                "configname": x.configname,
                "namespace": x.namespace.namespace,
                "configmap_k": x.configMap_k,
                "configmap_v": x.configMap_v,
            })
            # print(x.namespace.namespace)
            print(tmp)


