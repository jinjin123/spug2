from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import RancherNamespace,RancherConfigMap,RancherProject,RancherDeployment
import unittest


class Mytest(unittest.TestCase):
    def test_get_dev_project(self):
        url = settings.RANCHER_DEV_PRO_URL
        token = settings.RANCHER_DEV_TOKEN
        kwargs = {
            "url": url,
            "headers": {"Authorization": token, "Content-Type": "application/json"}
        }
        try:
            res = RequestApiAgent().list(**kwargs)
            datalist = (json.loads(res.content))["data"]
            project_bulk = []
            for x in datalist:
                # print(x["name"])
                if x["name"] != "kube-system" and x["name"] != "kube-public" and x["name"] != "kube-node-lease" and x["id"] != "local:p-zsr86":
                    project_bulk.append(RancherProject(
                        project_name=x["name"],
                        project_id=x["id"]
                    ))
            # print(project_bulk)
            RancherProject.objects.bulk_create(project_bulk)
            return res.status_code
        except Exception as e:
            print(e)
            return e

    def test_get_rancher(self):
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
                # print(x["name"])
                if x["name"] != "kube-system" and x["name"] != "kube-public" and x["name"] != "kube-node-lease" and x[
                    "projectId"] != "local:p-zsr86":
                    namespace_bulk.append(RancherNamespace(
                        project=RancherProject.objects.filter(project_id=x["projectId"]).first(),
                        namespace=x["name"],
                        # namespace_id=x["projectId"]
                        # env_id=1,
                        # create_by_id=1
                    ))
            # print(namespace_bulk)
            RancherNamespace.objects.bulk_create(namespace_bulk)
            return res.status_code
        except Exception as e:
            print(e)
            return e

    def test_get_configmap(self):
        ns = RancherProject.objects.all().values("project_id")
        for xx in ns:
            # print(x["namespace_id"])
            url = settings.RANCHER_DEV_CONFIGMAP.format(xx["project_id"])
            token = settings.RANCHER_DEV_TOKEN
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
                                  project=RancherProject.objects.filter(project_id=x["projectId"]).first(),
                                  namespace=RancherNamespace.objects.filter(namespace=x["namespaceId"]).first(),
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
                return e

    def test_get_rancher_svc(self):
        pj= RancherProject.objects.all().values("project_id")
        for xx in pj:
            url = settings.RANCHER_DEV_SVC_URL.format(xx["project_id"])
            token = settings.RANCHER_DEV_TOKEN
            kwargs = {
                "url": url,
                "headers": {"Authorization": token,"Content-Type": "application/json"}
            }
            try:
                res = RequestApiAgent().list(**kwargs)
                datalist = (json.loads(res.content))["data"]
                svc_bulk = []
                global x, v_name
                for x in datalist:
                    if x.get("volumes"):
                       volumes_v = x["volumes"]
                       for v_v in volumes_v:
                            if v_v.get("configMap"):
                                v_name = v_v["configMap"]["name"]
                            else:
                                v_name = "0"
                    else:
                       volumes_v = 0
                       v_name = "0"
                    if x.get("containers"):
                        cbox = x.get("containers")
                        img = [cc["image"] for cc in cbox]
                    if x.get("publicEndpoints"):
                        pp = x.get("publicEndpoints")
                        pubsvc = [{"address":x["addresses"],"port":x["port"] , "svcname": x["serviceId"]} for x in pp ]
                    else:
                        pubsvc = "0"


                    svc_bulk.append(RancherDeployment(
                            deployname=x["name"],
                            deployid=x["id"],
                            deploy_type=x["type"],
                            createts=x["createdTS"],
                            img=img[0],
                            pubsvc=pubsvc,
                            state=x["state"],
                            replica=x.get("scale",0),
                            volumes_detail=volumes_v,
                            volumes=v_name,
                            namespace=RancherNamespace.objects.filter(namespace=x["namespaceId"]).first(),
                            project=RancherProject.objects.filter(project_id=x["projectId"]).first()
                         )
                    )

                RancherDeployment.objects.bulk_create(svc_bulk)
            except Exception as e:
                print(x)
                print(e)
                return e
    def test(self):
        ns = RancherNamespace.objects.all().values("namespace_id")
        print(list(ns))
        conf = RancherNamespace.objects.filter(namespace='default').first()
        print(conf)
        print(list(conf)[0].project_id)
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



