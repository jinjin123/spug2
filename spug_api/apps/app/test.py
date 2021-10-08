from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import RancherNamespace, RancherConfigMap, RancherProject, RancherDeployment, RancherSvcPubStandby
from apps.config.models import RancherApiConfig
import unittest


class Mytest(unittest.TestCase):
    # def test_get_dev_project(self):
    #     url = settings.RANCHER_DEV_PRO_URL
    #     token = settings.RANCHER_DEV_TOKEN
    #     kwargs = {
    #         "url": url,
    #         "headers": {"Authorization": token, "Content-Type": "application/json"}
    #     }
    #     try:
    #         res = RequestApiAgent().list(**kwargs)
    #         datalist = (json.loads(res.content))["data"]
    #         project_bulk = []
    #         for x in datalist:
    #             # print(x["name"])
    #             if x["name"] != "kube-system" and x["name"] != "kube-public" and x["name"] != "kube-node-lease" and x["id"] != "local:p-zsr86":
    #                 project_bulk.append(RancherProject(
    #                     project_name=x["name"],
    #                     project_id=x["id"]
    #                 ))
    #         # print(project_bulk)
    #         RancherProject.objects.bulk_create(project_bulk)
    #         return res.status_code
    #     except Exception as e:
    #         print(e)
    #         return e
    #
    # def test_get_rancher(self):
    #     url = settings.RANCHER_DEV_NS_URL
    #     token = settings.RANCHER_DEV_TOKEN
    #     kwargs = {
    #         "url": url,
    #         "headers": {"Authorization": token, "Content-Type": "application/json"}
    #     }
    #     try:
    #         res = RequestApiAgent().list(**kwargs)
    #         datalist = (json.loads(res.content))["data"]
    #         namespace_bulk = []
    #         for x in datalist:
    #             # print(x["name"])
    #             if x["name"] != "kube-system" and x["name"] != "kube-public" and x["name"] != "kube-node-lease" and x[
    #                 "projectId"] != "local:p-zsr86":
    #                 namespace_bulk.append(RancherNamespace(
    #                     project=RancherProject.objects.filter(project_id=x["projectId"]).first(),
    #                     namespace=x["name"],
    #                     # namespace_id=x["projectId"]
    #                     # env_id=1,
    #                     # create_by_id=1
    #                 ))
    #         # print(namespace_bulk)
    #         RancherNamespace.objects.bulk_create(namespace_bulk)
    #         return res.status_code
    #     except Exception as e:
    #         print(e)
    #         return e
    #
    # def test_get_configmap(self):
    #     ns = RancherProject.objects.all().values("project_id")
    #     for xx in ns:
    #         # print(x["namespace_id"])
    #         url = settings.RANCHER_DEV_CONFIGMAP.format(xx["project_id"])
    #         token = settings.RANCHER_DEV_TOKEN
    #         kwargs = {
    #             "url": url,
    #             "headers": {"Authorization": token,"Content-Type": "application/json"}
    #         }
    #         # print(RancherNamespace.objects.filter(namespace_id=xx["namespace_id"])[:1])
    #         try:
    #             res = RequestApiAgent().list(**kwargs)
    #             datalist = (json.loads(res.content))["data"]
    #             config_bulk = []
    #             global x
    #             for x in datalist:
    #                 # print(x["name"])
    #                 if x.get("data",None):
    #                     for k,v in dict.items(x["data"]):
    #                         config_bulk.append(
    #                           RancherConfigMap(
    #                               project=RancherProject.objects.filter(project_id=x["projectId"]).first(),
    #                               namespace=RancherNamespace.objects.filter(namespace=x["namespaceId"]).first(),
    #                               configid=x["id"],
    #                               configname=x["name"],
    #                               configMap_k=k,
    #                               configMap_v=v
    #                           )
    #                         )
    #                 # print(type(x["data"]))
    #             RancherConfigMap.objects.bulk_create(config_bulk)
    #         except Exception as e:
    #             print(x)
    #             print(e)
    #             return e
    #
    # def test_get_rancher_svc(self):
    #     pj= RancherProject.objects.all().values("project_id")
    #     for xx in pj:
    #         url = settings.RANCHER_DEV_SVC_URL.format(xx["project_id"])
    #         token = settings.RANCHER_DEV_TOKEN
    #         kwargs = {
    #             "url": url,
    #             "headers": {"Authorization": token,"Content-Type": "application/json"}
    #         }
    #         try:
    #             res = RequestApiAgent().list(**kwargs)
    #             datalist = (json.loads(res.content))["data"]
    #             svc_bulk = []
    #             global x, v_name
    #             for x in datalist:
    #                 if x.get("volumes"):
    #                    volumes_v = x["volumes"]
    #                    for v_v in volumes_v:
    #                         if v_v.get("configMap"):
    #                             v_name = v_v["configMap"]["name"]
    #                         else:
    #                             v_name = "0"
    #                 else:
    #                    volumes_v = 0
    #                    v_name = "0"
    #                 if x.get("containers"):
    #                     cbox = x.get("containers")
    #                     img = [cc["image"] for cc in cbox]
    #                 if x.get("publicEndpoints"):
    #                     pp = x.get("publicEndpoints")
    #                     pubsvc = [{"address":x["addresses"],"port":x["port"] , "svcname": x["serviceId"]} for x in pp ]
    #                 else:
    #                     pubsvc = "0"
    #
    #
    #                 svc_bulk.append(RancherDeployment(
    #                         deployname=x["name"],
    #                         deployid=x["id"],
    #                         deploy_type=x["type"],
    #                         createts=x["createdTS"],
    #                         img=img[0],
    #                         pubsvc=pubsvc,
    #                         state=x["state"],
    #                         replica=x.get("scale",0),
    #                         volumes_detail=volumes_v,
    #                         volumes=v_name,
    #                         namespace=RancherNamespace.objects.filter(namespace=x["namespaceId"]).first(),
    #                         project=RancherProject.objects.filter(project_id=x["projectId"]).first()
    #                      )
    #                 )
    #
    #             RancherDeployment.objects.bulk_create(svc_bulk)
    #         except Exception as e:
    #             print(x)
    #             print(e)
    #             return e
    # def test(self):
    #     publish_args = RancherSvcPubStandby.objects.filter(app_id=38).first()
    #     print((publish_args.to_dict())['project_id'])
    # ns = RancherNamespace.objects.all().values("namespace_id")
    # print(list(ns))
    # conf = RancherNamespace.objects.filter(namespace='default').first()
    # print(conf)
    # print(list(conf)[0].project_id)
    # tmp= []
    # for x in conf:
    #     tmp.append({
    #         "id":x.id,
    #         "configid": x.configid,
    #         "configname": x.configname,
    #         "namespace": x.namespace.namespace,
    #         "configmap_k": x.configMap_k,
    #         "configmap_v": x.configMap_v,
    #     })
    #     # print(x.namespace.namespace)
    #     print(tmp)

    def test(self):
        # global img
        # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT").first()
        # ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS").first()
        # cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP").first()
        # svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC").first()
        # pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC").first()
        pj = RancherApiConfig.objects.filter(env_id=1, label="GETPROJECT").first()
        ns = RancherApiConfig.objects.filter(env_id=1, label="GETNS").first()
        cmap = RancherApiConfig.objects.filter(env_id=1, label="GETCONFIGMAP").first()
        svc = RancherApiConfig.objects.filter(env_id=1, label="GETSVC").first()
        pvc = RancherApiConfig.objects.filter(env_id=1, label="GETPVC").first()
        url = pj.url
        token = pj.token
        kwargs = {
            "url": url,
            "headers": {"Authorization": token, "Content-Type": "application/json"}
        }
        res = RequestApiAgent().list(**kwargs)
        pjdatalist = (json.loads(res.content))["data"]
        pjnew = []
        for x in pjdatalist:
            # if x["id"] == "local:p-9s8fj" or x["id"] == "local:p-f9tqd" or x["id"] == "local:p-8v6qj" or x["id"] == "local:p-t48wr" or x["id"] == "local:p-486kn" \
            #         or x["id"] == "local:p-9s8fj":
            if x["id"] == "local:p-cvfqn":
                pjnew.append({"pjid": x["id"], "pjname": x["name"]})
            # print(x["id"],x["name"])
        # print(len(pjnew))
        url = ns.url
        token = ns.token
        kwargs = {
            "url": url,
            "headers": {"Authorization": token, "Content-Type": "application/json"}
        }
        res = RequestApiAgent().list(**kwargs)
        nsdatalist = (json.loads(res.content))["data"]
        nsnew = []
        for x in nsdatalist:
            nsnew.append({"pjid": x["projectId"], "nsid": x["id"], "nsname": x["name"]})
            # print(x["projectId"],x["id"], x["name"])
        # print(nsnew)
        nspj = []
        for x in nsnew:
            for xx in pjnew:
                if x["pjid"] == xx["pjid"]:
                    nspj.append({"pjid": x["pjid"], "nsid": x["nsid"], "nsname": x["nsname"], "pjname": xx["pjname"]})
        # print(len(nspj))
        print(nspj)
        # -----------------------------------------------------------------------------
        url = svc.url
        token = svc.token
        svcnew = []
        for sx in nspj:
            kwargs = {
                "url": url.format(sx["pjid"]),
                "headers": {"Authorization": token, "Content-Type": "application/json"}
            }
            res = RequestApiAgent().list(**kwargs)
            svcdatalist = (json.loads(res.content))["data"]
            for svcdict in svcdatalist:
                # for xxx in nspj:
                if svcdict["projectId"].strip() == sx["pjid"].strip() and svcdict["namespaceId"].strip() == sx["nsid"]:
                    global img, v_name, pvcid,pubsvc
                    img = []
                    if svcdict.get("containers"):
                        cbox = svcdict.get("containers")
                        img = [cc["image"] for cc in cbox]

                    if svcdict.get("volumes"):
                        volumes_v = svcdict["volumes"]
                        tmppvcid = []
                        for v_v in volumes_v:
                            if v_v.get("configMap"):
                                v_name = v_v["configMap"]["name"]
                            else:
                                v_name = ""
                            if v_v.get("persistentVolumeClaim"):
                                tmppvcid.append(v_v.get("persistentVolumeClaim").get("persistentVolumeClaimId"))
                        pvcid = ",".join(tmppvcid)
                    if svcdict.get("publicEndpoints"):
                        pp = svcdict.get("publicEndpoints")
                        pubsvc = [{"address":x["addresses"],"port":x["port"] , "svcname": x["serviceId"]} for x in pp]
                    else:
                        pubsvc = ""
                    svcnew.append({"pjid": svcdict["projectId"], "pjname": sx["pjname"],
                                    "nsid": svcdict["namespaceId"], "nsname": sx["nsname"],
                                    "dpid": svcdict["id"], "dpname": svcdict["name"],
                                    "img": img[0], "replica": svcdict.get("scale",0),
                                    "configName": v_name,"configId":"","configMap":"","pvcid": pvcid ,"rancher_url":"https://rancher.ioc.com/","pubsvc": pubsvc})
                # else:
                    # print(svcdict["projectId"],sx["pjid"])
                    # pass
        print(len(svcnew))

        url = cmap.url
        token = cmap.token
        cmapnew = []
        for cx in svcnew:
            kwargs = {
                "url": url.format(cx["pjid"]),
                "headers": {"Authorization": token, "Content-Type": "application/json"}
            }
            res = RequestApiAgent().list(**kwargs)
            mpdatalist = (json.loads(res.content))["data"]
            for xxx in mpdatalist:
                # print(xxx["name"])
                global  kvtmp
                if cx["configName"].strip() !="":
                    if xxx["name"].strip() == cx["configName"].strip():
                        if xxx.get("data",None):
                            kvtmp = []
                            for k,v in dict.items(xxx["data"]):
                                kvtmp.append({k,v})
                                cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
                                                "nsid": cx["nsid"], "nsname": cx["nsname"],
                                                "dpid": cx["dpid"], "dpname": cx["dpname"],
                                                "img": cx["img"], "replica": cx["replica"],
                                                "configName": cx["configName"],"configId": xxx["id"],"configMap":kvtmp,
                                                "pvcid": cx["pvcid"],
                                                "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"],
                                                })
            if cx["configName"].strip() =="":
                cmapnew.append(cx)
                # print(cx["dpname"])
                    # cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
                    #                             "nsid": cx["nsid"], "nsname": cx["nsname"],
                    #                             "dpid": cx["dpid"], "dpname": cx["dpname"],
                    #                             "img": cx["img"], "replica": cx["replica"],
                    #                             "configName": cx["configName"],"configId": "","configMap":"",
                    #                             "pvcid": cx["pvcid"],
                    #                             "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"]})
                # else:
                #     cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
                #                         "nsid": cx["nsid"], "nsname": cx["nsname"],
                #                         "dpid": cx["dpid"], "dpname": cx["dpname"],
                #                         "img": cx["img"], "replica": cx["replica"],
                #                         "configName": cx["configName"],"configId": xxx["id"],"configMap":kvtmp,
                #                         "pvcid": cx["pvcid"],
                #                         "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"],})
                    # print(xxx["projectId"],cx["pjid"],xxx["name"],cx["configName"])
        print(len(cmapnew))

        url = pvc.url
        token = pvc.token
        pvcnew = []
        for px in cmapnew:
            kwargs = {
                "url": url.format(px["pjid"]),
                "headers": {"Authorization": token, "Content-Type": "application/json"}
            }
            res = RequestApiAgent().list(**kwargs)
            pvdatalist = (json.loads(res.content))["data"]
            for xxx in pvdatalist:
                if xxx["id"].strip() == px["pvcid"].strip():
                        pvcnew.append({"pjid": px["pjid"], "pjname": px["pjname"],
                                        "nsid": px["nsid"], "nsname": px["nsname"],
                                        "dpid": px["dpid"], "dpname": px["dpname"],
                                        "img": px["img"], "replica": px["replica"],
                                        "configName": px["configName"],"configId": px["configId"],"configMap":px["configMap"],
                                        "pvcid": px["pvcid"],"pvcsize": xxx.get("resources").get("requests").get("storage"),
                                        "rancher_url":px["rancher_url"],"pubsvc": px["pubsvc"],
                                        })
                else:
                   pvcnew.append(px)

        print(len(pvcnew))
