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


    # def test(self):
    #     from apps.host.models import Host
    #     import math
    #     iplist = ["10.145.188.134", "10.147.3.65", " 19.104.40.35", " 19.104.48.33", " 19.104.50.124", "19.104.50.60",
    #      " 19.104.53.124", "19.104.53.219", "19.106.85.10", "19.106.85.26", "19.106.85.68", "10.145.188.135",
    #      "10.147.3.66", " 19.104.40.36", " 19.104.49.142", "19.104.50.125", "19.104.50.72", " 19.104.53.126",
    #      "19.104.53.48", " 19.106.85.11", "19.106.85.27", "19.106.85.69", "10.146.0.53", " 10.147.3.67",
    #      " 19.104.40.37", " 19.104.49.143", "19.104.50.131", "19.104.50.73", " 19.104.53.129", "19.104.53.53",
    #      " 19.106.85.12", "19.106.85.28", "19.106.85.7", "10.147.1.128", "10.147.3.68", " 19.104.40.38",
    #      " 19.104.49.144", "19.104.50.139", "19.104.50.74", " 19.104.53.130", "19.104.53.54", " 19.106.85.13",
    #      "19.106.85.29", "19.106.85.70", "10.147.1.129", "10.147.4.247", "19.104.40.40", " 19.104.49.145",
    #      "19.104.50.141", "19.104.50.75", " 19.104.53.131", "19.104.53.55", " 19.106.85.14", "19.106.85.3",
    #      " 19.106.85.72", "10.147.1.130", "19.104.40.14", "19.104.40.46", " 19.104.49.146", "19.104.50.142",
    #      "19.104.50.76", " 19.104.53.132", "19.104.53.56", " 19.106.85.15", "19.106.85.30", "19.106.85.73",
    #      "10.147.2.49", " 19.104.40.15", "19.104.40.8", "19.104.49.147", "19.104.50.155", "19.104.50.77",
    #      " 19.104.53.133", "19.104.53.57", " 19.106.85.16", "19.106.85.31", "19.106.85.74", "10.147.2.50",
    #      " 19.104.40.19", "19.104.40.9", "19.104.49.148", "19.104.50.160", "19.104.50.86", " 19.104.53.134",
    #      "19.104.53.58", " 19.106.85.17", "19.106.85.32", "19.106.85.8", "10.147.2.51", " 19.104.40.21",
    #      "19.104.44.194", "19.104.49.149", "19.104.50.181", "19.104.51.125", "19.104.53.135", "19.104.53.59",
    #      " 19.106.85.18", "19.106.85.33", "19.106.85.9", "10.147.2.52", " 19.104.40.23", "19.104.44.195",
    #      "19.104.49.150", "19.104.50.188", "19.104.51.126", "19.104.53.136", "19.104.53.60", " 19.106.85.19",
    #      "19.106.85.34", "10.147.2.58", " 19.104.40.24", "19.104.44.196", "19.104.49.151", "19.104.50.195",
    #      "19.104.51.127", "19.104.53.137", "19.104.53.61", " 19.106.85.2", " 19.106.85.35", "10.147.3.246",
    #      "19.104.40.29", "19.104.44.197", "19.104.50.1", "19.104.50.204", "19.104.51.128", "19.104.53.138",
    #      "19.104.53.62", " 19.106.85.20", "19.106.85.36", "10.147.3.60", " 19.104.40.30", "19.104.44.198",
    #      "19.104.50.109", "19.104.50.210", "19.104.51.129", "19.104.53.213", "19.104.53.63", " 19.106.85.21",
    #      "19.106.85.37", "10.147.3.61", " 19.104.40.31", "19.104.44.199", "19.104.50.11", " 19.104.50.219",
    #      "19.104.51.149", "19.104.53.214", "19.104.53.64", " 19.106.85.22", "19.106.85.38", "10.147.3.62",
    #      " 19.104.40.32", "19.104.48.30", " 19.104.50.116", "19.104.50.227", "19.104.52.95", " 19.104.53.215",
    #      "19.104.59.1", "19.106.85.23", "19.106.85.4", "10.147.3.63", " 19.104.40.33", "19.104.48.31", " 19.104.50.118",
    #      "19.104.50.43", " 19.104.53.122", "19.104.53.216", "19.104.59.2", "19.106.85.24", "19.106.85.5", "10.147.3.64",
    #      " 19.104.40.34", "19.104.48.32", " 19.104.50.121", "19.104.50.55", " 19.104.53.123", "19.104.53.217",
    #      "19.104.59.3", "19.106.85.25", "19.106.85.6"]
    #     for x in iplist:
    #         try:
    #             with open("/home/jin/cmdbv3/spug/spug_api/out/"+x.strip()) as f:
    #             # with open("/home/jin/cmdbv3/spug/spug_api/out/" + "19.104.51.129") as f:
    #                 a = f.read()
    #                 ser = json.loads(a)
    #                 # print(ser["ansible_facts"]["ansible_mounts"])
    #                 # for x in ser["ansible_facts"]["ansible_mounts"]:
    #                 #     print(x["size_total"])
    #
    #                 Host.objects.create(
    #                     ipaddress=[ x  for x in ser["ansible_facts"]["ansible_all_ipv4_addresses"] if not x.startswith("192.168") ][0],
    #                     osType=ser["ansible_facts"]["ansible_distribution"],
    #                     osVerion=ser["ansible_facts"]["ansible_distribution_version"],
    #                     coreVerion=ser["ansible_facts"]["ansible_kernel"],
    #                     disk=[{"type": x["fstype"],"name":x["device"],"mount":x["mount"],"size": math.ceil(x.get("size_total",0) / 1024 /1024/1024) }  for x in ser["ansible_facts"]["ansible_mounts"]],
    #                     disks=len(ser["ansible_facts"]["ansible_mounts"]),
    #                     # memory= int(ser["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
    #                     memory=math.ceil(ser["ansible_facts"]["ansible_memtotal_mb"] / 1024 ),
    #                     cpus=ser["ansible_facts"]["ansible_processor_count"],
    #                     cpucore=ser["ansible_facts"]["ansible_processor_cores"],
    #                     hostname=ser["ansible_facts"]["ansible_nodename"],
    #                     supplier=ser["ansible_facts"]["ansible_system_vendor"],
    #                 )
    #         except Exception as e:
    #             print(e,x)
                # print((json.loads(a))["ansible_facts"]["ansible_all_ipv4_addresses"])