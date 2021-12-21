from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import *
from django.db.models import Q,Count
from apps.config.models import RancherApiConfig
import unittest
from django.core.mail import send_mail
from apps.host.models import *
from apps.config.models import *

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

    # def test(self):
    # #     # global img
    # #     pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT").first()
    # #     ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS").first()
    # #     # cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP").first()
    # #     # svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC").first()
    # #     # pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC").first()
    #     pj = RancherApiConfig.objects.filter(env_id=2, label="GETSIGPROJECT",tag="ioc").first()
    #     ns = RancherApiConfig.objects.filter(env_id=2, label="GETSIGNS",tag="ioc").first()
    # #     pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT",tag="ioc").first()
    # #     ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS",tag="ioc").first()
    #     cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP",tag="ioc").first()
    #     svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="ioc").first()
    #     pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC",tag="ioc").first()
    #     url = pj.url
    #     token = pj.token
    #     kwargs = {
    #         "url": url,
    #         "headers": {"Authorization": token, "Content-Type": "application/json"}
    #     }
    #     res = RequestApiAgent().list(**kwargs)
    #     pjdatalist = (json.loads(res.content))["data"]
    #     pjnew = []
    #     for x in pjdatalist:
    #         # if x["id"] == "local:p-9s8fj" or x["id"] == "local:p-f9tqd" or x["id"] == "local:p-8v6qj" or x["id"] == "local:p-t48wr" or x["id"] == "local:p-486kn" or x["id"] == "local:p-9s8fj":
    #         # if x["id"] == "local:p-9s8fj" or x["id"] == "local:p-f9tqd" or x["id"] == "local:p-8v6qj":
    #         # if x["id"] == "local:p-cvfqn":
    #         #-----
    #         # if x["id"] == "local:p-9s8fj" or x["id"] == "local:p-f9tqd" or x["id"] == "local:p-8v6qj":
    #         #     pjnew.append({"pjid": x["id"], "pjname": x["name"],"top_project":"东莞市政务数据大脑暨智慧城市IOC运行中心建设项目","toppjid":"dgdataheadioc"})
    #         # if x["id"] == "local:p-t48wr":
    #         #     pjnew.append({"pjid": x["id"], "pjname": x["name"], "top_project": "疫情地图项目","toppjid": "dgcovidmap"})
    #         #------
    #         if x['id']  == 'c-5tk6p:p-55knm':
    #                 pjnew.append({"pjid": x['id'], "pjname":x['name'],"top_project": "test","toppjid": "test"})
    #         # print(x["id"],x["name"])
    #     print(len(pjnew))
    #     url = ns.url
    #     token = ns.token
    #     kwargs = {
    #         "url": url,
    #         "headers": {"Authorization": token, "Content-Type": "application/json"}
    #     }
    #     res = RequestApiAgent().list(**kwargs)
    #     nsdatalist = (json.loads(res.content))["data"]
    #     nsnew = []
    #     for x in nsdatalist:
    #         #------
    #         if x['id'] == 'spug':
    #             nsnew.append({"pjid": x["projectId"], "nsid": x["id"], "nsname": x["name"]})
    #         #-------
    #         # nsnew.append({"pjid": x["projectId"], "nsid": x["id"], "nsname": x["name"]})
    #         # print(x["projectId"],x["id"], x["name"])
    #     # print(nsnew)
    #     nspj = []
    #     for x in nsnew:
    #         for xx in pjnew:
    #             if x["pjid"] == xx["pjid"]:
    #                 x.update({"pjname": xx["pjname"],"top_project":xx["top_project"],"toppjid":xx["toppjid"]})
    #                 nspj.append(x)
    #     print(len(nspj))
    #     # print(nspj)
    #     # -----------------------------------------------------------------------------
    #     url = svc.url
    #     token = svc.token
    #     svcnew = []
    #     for sx in nspj:
    #         kwargs = {
    #             "url": url.format(sx["pjid"]),
    #             "headers": {"Authorization": token, "Content-Type": "application/json"}
    #         }
    #         res = RequestApiAgent().list(**kwargs)
    #         svcdatalist = (json.loads(res.content))["data"]
    #         for svcdict in svcdatalist:
    #             # for xxx in nspj:
    #             if svcdict["projectId"].strip() == sx["pjid"].strip() and svcdict["namespaceId"].strip() == sx["nsid"]:
    #                 global img, v_name, pubsvc, cbox_env, v_mount, volumes_v,cports
    #                 img = []
    #                 if svcdict.get("containers"):
    #                     cbox = svcdict.get("containers")
    #                     img = [cc["image"] for cc in cbox]
    #                     cbox_env = [cenv["environment"] for cenv in cbox if cenv.get("environment", "")]
    #                     v_mount = [vm["volumeMounts"] for vm in cbox if vm.get("volumeMounts",[])]
    #                     cports = [vm["ports"] for vm in cbox if vm.get("ports",[])]
    #
    #                 if svcdict.get("volumes"):
    #                     volumes_v = svcdict["volumes"]
    #                     tmppvcid = []
    #                     for v_v in volumes_v:
    #                         if v_v.get("configMap"):
    #                             v_name = v_v["configMap"]["name"]
    #                         else:
    #                             v_name = ""
    #                         # if v_v.get("persistentVolumeClaim"):
    #                         #     tmppvcid.append(v_v.get("persistentVolumeClaim").get("persistentVolumeClaimId"))
    #                     pvcid = ",".join(tmppvcid)
    #                 if svcdict.get("publicEndpoints"):
    #                     pp = svcdict.get("publicEndpoints")
    #                     pubsvc = [{"address":x["addresses"],"port":x["port"] , "svcname": x["serviceId"]} for x in pp]
    #                 else:
    #                     pubsvc = ""
    #                 svcnew.append({"top_project":sx["top_project"],"toppjid":sx["toppjid"],"pjid": svcdict["projectId"], "pjname": sx["pjname"],
    #                                 "nsid": svcdict["namespaceId"], "nsname": sx["nsname"],
    #                                 "dpid": svcdict["id"], "dpname": svcdict["name"],
    #                                 "img": img[0], "replica": svcdict.get("scale",0), "state":svcdict["state"] ,
    #                                 # "configName": v_name,"configId":"","configMap":"","pvcid": pvcid ,"rancher_url":"https://rancher.ioc.com/","pubsvc": pubsvc})
    #                                 "configName": v_name, "configId": "", "configMap": "", "volumes":volumes_v,"v_mount": v_mount[0] if len(v_mount) >0 else [],"cbox_env": cbox_env,
    #                                "rancher_url": "https://rancher.ioc.com/", "pubsvc": pubsvc,"verifyurl": "https://rancher.ioc.com/" + 'p/'+ svcdict["projectId"] + "/workload/"+ svcdict["id"],
    #                                 "cports": cports,"pauselinks":svcdict['actions']['pause'],"rdplinks":svcdict['actions']['redeploy'],"rollbacklinks":svcdict['actions']['rollback'],"updatelinks":svcdict['links']['update'],
    #                                 "removelinks":svcdict['links']['remove'],"revisionslinks":svcdict['links']['revisions'],
    #                                "statuslinks":((RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="ioc").first()).url).format(svcdict['projectId']) + "/" +svcdict['id']})
    #             # else:
    #                 # print(svcdict["projectId"],sx["pjid"])
    #                 # pass
    #
    #     url = cmap.url
    #     token = cmap.token
    #     cmapnew = []
    #     for cx in svcnew:
    #         kwargs = {
    #             "url": url.format(cx["pjid"]),
    #             "headers": {"Authorization": token, "Content-Type": "application/json"}
    #         }
    #         res = RequestApiAgent().list(**kwargs)
    #         mpdatalist = (json.loads(res.content))["data"]
    #         for xxx in mpdatalist:
    #             # print(xxx["name"])
    #             global  kvtmp
    #             if cx["configName"].strip() !="":
    #                 if xxx["name"].strip() == cx["configName"].strip():
    #                     if xxx.get("data",None):
    #                         kvtmp = []
    #                         for k,v in dict.items(xxx["data"]):
    #                             kvtmp.append({"k":k,"v":v})
    #                             cmapnew.append(ProjectService(**{"top_project":cx["top_project"],"toppjid":cx["toppjid"],"pjid": cx["pjid"], "pjname": cx["pjname"],
    #                                             "nsid": cx["nsid"], "nsname": cx["nsname"],
    #                                             "dpid": cx["dpid"], "dpname": cx["dpname"],
    #                                             "img": cx["img"], "replica": cx["replica"],"state":cx["state"],
    #                                             "configName": cx["configName"],"configId": xxx["id"],"configMap":kvtmp,
    #                                             # "pvcid": cx["pvcid"],
    #                                             "volumes": cx["volumes"], "v_mount": cx["v_mount"],"cbox_env": cx["cbox_env"],
    #                                             "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"],"verifyurl": cx["verifyurl"], "env_id":2,
    #                                             "cports": cx["cports"],"pauselinks":cx["pauselinks"],"rdplinks":cx["rdplinks"],"rollbacklinks": cx["rollbacklinks"], "updatelinks": cx["updatelinks"],
    #                                             "removelinks": cx["removelinks"], "revisionslinks": cx["revisionslinks"],"statuslinks":cx["statuslinks"]
    #                                             }))
    #         if cx["configName"].strip() =="":
    #             cx.update({"configMap": "[]"})
    #             cmapnew.append(ProjectService(**cx))
    #
    #     try:
    #         ProjectService.objects.bulk_create(cmapnew)
    #     except Exception as e:
    #         print(e)
        # ---------------------------------------
        #         print(cx["dpname"])
        #             cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
        #                                         "nsid": cx["nsid"], "nsname": cx["nsname"],
        #                                         "dpid": cx["dpid"], "dpname": cx["dpname"],
        #                                         "img": cx["img"], "replica": cx["replica"],
        #                                         "configName": cx["configName"],"configId": "","configMap":"",
        #                                         "pvcid": cx["pvcid"],
        #                                         "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"]})
        #         else:
        #             cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
        #                                 "nsid": cx["nsid"], "nsname": cx["nsname"],
        #                                 "dpid": cx["dpid"], "dpname": cx["dpname"],
        #                                 "img": cx["img"], "replica": cx["replica"],
        #                                 "configName": cx["configName"],"configId": xxx["id"],"configMap":kvtmp,
        #                                 "pvcid": cx["pvcid"],
        #                                 "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"],})
        #             print(xxx["projectId"],cx["pjid"],xxx["name"],cx["configName"])
        # print(len(cmapnew))
        #
        # url = pvc.url
        # token = pvc.token
        # pvcnew = []
        # for px in cmapnew:
        #     kwargs = {
        #         "url": url.format(px["pjid"]),
        #         "headers": {"Authorization": token, "Content-Type": "application/json"}
        #     }
        #     res = RequestApiAgent().list(**kwargs)
        #     pvdatalist = (json.loads(res.content))["data"]
        #     for xxx in pvdatalist:
        #         if xxx["id"].strip() == px["pvcid"].strip():
        #                 pvcnew.append(ProjectService(**{"top_project":px["top_project"],"toppjid":px["toppjid"],"pjid": px["pjid"], "pjname": px["pjname"],
        #                                 "nsid": px["nsid"], "nsname": px["nsname"],
        #                                 "dpid": px["dpid"], "dpname": px["dpname"],
        #                                 "img": px["img"], "replica": px["replica"],"state":px["state"] ,
        #                                 "configName": px["configName"],"configId": px["configId"],"configMap":px["configMap"],
        #                                 "pvcid": px["pvcid"],"pvcsize": xxx.get("resources").get("requests").get("storage"),
        #                                 "rancher_url":px["rancher_url"],"pubsvc": px["pubsvc"],
        #                                 }))
        #         else:
        #            pvcnew.append(ProjectService(**px))
        #
        # try:
        #     ProjectService.objects.bulk_create(pvcnew)
        # except Exception as e :
        #     print(e)

        # print(pvcnew[:1])

    # def test_fanyi(self):
    #         # global img
    #         # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT").first()
    #         # ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS").first()
    #         # cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP").first()
    #         # svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC").first()
    #         # pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC").first()
    #
    #         # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT",tag="feiyan").first()
    #         # ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS",tag="feiyan").first()
    #         # cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP",tag="feiyan").first()
    #         # svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="feiyan").first()
    #         # pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC",tag="feiyan").first()
    #
    #         pj = RancherApiConfig.objects.filter(env_id=2, label="GETPROJECT", tag="feiyanuos").first()
    #         ns = RancherApiConfig.objects.filter(env_id=2, label="GETNS", tag="feiyanuos").first()
    #         cmap = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP", tag="feiyanuos").first()
    #         svc = RancherApiConfig.objects.filter(env_id=2, label="GETSVC", tag="feiyanuos").first()
    #         pvc = RancherApiConfig.objects.filter(env_id=2, label="GETPVC", tag="feiyanuos").first()
    #         url = pj.url
    #         token = pj.token
    #         kwargs = {
    #             "url": url,
    #             "headers": {"Authorization": token, "Content-Type": "application/json"}
    #         }
    #         res = RequestApiAgent().list(**kwargs)
    #         pjdatalist = (json.loads(res.content))["data"]
    #         pjnew = []
    #         for x in pjdatalist:
    #             # if x["id"] == "local:p-qzsv4":
    #             #     pjnew.append({"pjid": x["id"], "pjname": x["name"],"top_project":"东莞市跨境货车司机信息管理系统项","toppjid":"dgdriverinfo"})
    #             # if x["id"] == "local:p-nglhq":
    #             #     pjnew.append({"pjid": x["id"], "pjname": x["name"],"top_project":"东莞市疫情动态查询+防控数据管理平台系统项目","toppjid":"dgdycovidselect"})
    #             #----------  uos
    #             if x["id"] == "local:p-b2gkq":
    #                 pjnew.append({"pjid": x["id"], "pjname": x["name"],"top_project":"东莞市跨境货车司机信息管理系统项","toppjid":"dgdriverinfo"})
    #             if x["id"] == "local:p-vlzv8":
    #                 pjnew.append({"pjid": x["id"], "pjname": x["name"],"top_project":"东莞市疫情动态查询+防控数据管理平台系统项目","toppjid":"dgdycovidselect"})
    #             #------------
    #             # print(x["id"],x["name"])
    #         # print(len(pjnew))
    #         url = ns.url
    #         token = ns.token
    #         kwargs = {
    #             "url": url,
    #             "headers": {"Authorization": token, "Content-Type": "application/json"}
    #         }
    #         res = RequestApiAgent().list(**kwargs)
    #         nsdatalist = (json.loads(res.content))["data"]
    #         nsnew = []
    #         for x in nsdatalist:
    #             nsnew.append({"pjid": x["projectId"], "nsid": x["id"], "nsname": x["name"]})
    #             # print(x["projectId"],x["id"], x["name"])
    #         # print(nsnew)
    #         nspj = []
    #         for x in nsnew:
    #             for xx in pjnew:
    #                 if x["pjid"] == xx["pjid"]:
    #                     x.update({"pjname": xx["pjname"],"top_project":xx["top_project"],"toppjid":xx["toppjid"]})
    #                     nspj.append(x)
    #                     # nspj.append(
    #                     #     {"pjid": x["pjid"], "nsid": x["nsid"], "nsname": x["nsname"], "pjname": xx["pjname"]})
    #         # print(len(nspj))
    #         # print(nspj)
    #         # -----------------------------------------------------------------------------
    #         url = svc.url
    #         token = svc.token
    #         svcnew = []
    #         for sx in nspj:
    #             kwargs = {
    #                 "url": url.format(sx["pjid"]),
    #                 "headers": {"Authorization": token, "Content-Type": "application/json"}
    #             }
    #             res = RequestApiAgent().list(**kwargs)
    #             svcdatalist = (json.loads(res.content))["data"]
    #             for svcdict in svcdatalist:
    #                 # for xxx in nspj:
    #                 if svcdict["projectId"].strip() == sx["pjid"].strip() and svcdict["namespaceId"].strip() == sx[
    #                     "nsid"]:
    #                     global img, v_name,  pubsvc,cbox_env,v_mount,volumes_v,cports
    #                     img = []
    #                     if svcdict.get("containers"):
    #                         cbox = svcdict.get("containers")
    #                         img = [cc["image"] for cc in cbox]
    #                         cbox_env = [cenv["environment"] for cenv in cbox  if cenv.get("environment","")]
    #                         v_mount = [vm["volumeMounts"] for vm in cbox if vm.get("volumeMounts",[])]
    #                         cports = [vm["ports"] for vm in cbox if vm.get("ports",[])]
    #
    #                     if svcdict.get("volumes"):
    #                         volumes_v = svcdict["volumes"]
    #                         # tmppvcid = []
    #                         for v_v in volumes_v:
    #                             if v_v.get("configMap"):
    #                                 v_name = v_v["configMap"]["name"]
    #                             else:
    #                                 v_name = ""
    #                             # if v_v.get("persistentVolumeClaim"):
    #                             #     tmppvcid.append(v_v.get("persistentVolumeClaim").get("persistentVolumeClaimId"))
    #                         # pvcid = ",".join(tmppvcid)
    #                     if svcdict.get("publicEndpoints"):
    #                         pp = svcdict.get("publicEndpoints")
    #                         pubsvc = [{"address": x["addresses"], "port": x["port"], "svcname": x["serviceId"]} for x in pp]
    #                     else:
    #                         pubsvc = ""
    #                     svcnew.append({"top_project":sx["top_project"],"toppjid":sx["toppjid"],"pjid": svcdict["projectId"], "pjname": sx["pjname"],
    #                                    "nsid": svcdict["namespaceId"], "nsname": sx["nsname"],
    #                                    "dpid": svcdict["id"], "dpname": svcdict["name"],
    #                                    "img": img[0], "replica": svcdict.get("scale", 0),"state":svcdict["state"],
    #                                    # "configName": v_name, "configId": "", "configMap": "", "pvcid": pvcid,
    #                                    "configName": v_name, "configId": "", "configMap": "", "volumes":volumes_v,"v_mount":v_mount[0] if len(v_mount) >0 else [],"cbox_env": cbox_env,
    #                                    # "rancher_url": "https://rancher.feiyan.com/", "pubsvc": pubsvc, "verifyurl": "https://rancher.feiyan.com/" + 'p/'+ svcdict["projectId"] + "/workload/"+ svcdict["id"],
    #                                    "rancher_url": "https://rancher.feiyan.uos.com/", "pubsvc": pubsvc, "verifyurl": "https://rancher.feiyan.uos.com/" + 'p/'+ svcdict["projectId"] + "/workload/"+ svcdict["id"],
    #                                    "cports": cports, "pauselinks": svcdict['actions']['pause'],
    #                                    "env_id": 2,
    #                                    "rdplinks": svcdict['actions']['redeploy'],
    #                                    "rollbacklinks": svcdict['actions']['rollback'],
    #                                    "updatelinks": svcdict['links']['update'],
    #                                    "removelinks": svcdict['links']['remove'],
    #                                    "revisionslinks": svcdict['links']['revisions'],
    #                                    # "statuslinks": ((RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="feiyan").first()).url).format(svcdict['projectId']) + "/" + svcdict['id']
    #                                    "statuslinks": ((RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="feiyanuos").first()).url).format(svcdict['projectId']) + "/" + svcdict['id']
    #                                    })
    #                 # else:
    #                 # print(svcdict["projectId"],sx["pjid"])
    #                 # pass
    #         # print(len(svcnew))
    #
    #         url = cmap.url
    #         token = cmap.token
    #         cmapnew = []
    #         for cx in svcnew:
    #             kwargs = {
    #                 "url": url.format(cx["pjid"]),
    #                 "headers": {"Authorization": token, "Content-Type": "application/json"}
    #             }
    #             res = RequestApiAgent().list(**kwargs)
    #             mpdatalist = (json.loads(res.content))["data"]
    #             for xxx in mpdatalist:
    #                 # print(xxx["name"])
    #                 global kvtmp
    #                 if cx["configName"].strip() != "":
    #                     if xxx["name"].strip() == cx["configName"].strip():
    #                         if xxx.get("data", None):
    #                             kvtmp = []
    #                             for k, v in dict.items(xxx["data"]):
    #                                 kvtmp.append({"k":k,"v":v})
    #                                 cmapnew.append(ProjectService(**{"top_project":cx["top_project"],"toppjid":cx["toppjid"],"pjid": cx["pjid"], "pjname": cx["pjname"],
    #                                                 "nsid": cx["nsid"], "nsname": cx["nsname"],
    #                                                 "dpid": cx["dpid"], "dpname": cx["dpname"],
    #                                                 "img": cx["img"], "replica": cx["replica"],"state":cx["state"] ,
    #                                                 "configName": cx["configName"], "configId": xxx["id"],
    #                                                 "configMap": kvtmp,
    #                                                 "volumes": cx["volumes"],"v_mount": cx["v_mount"],"cbox_env": cx["cbox_env"],
    #                                                 # "pvcid": cx["pvcid"],
    #                                                 "rancher_url": cx["rancher_url"], "pubsvc": cx["pubsvc"],"verifyurl": cx["verifyurl"],"env_id":2,
    #                                             "cports": cx["cports"],"pauselinks":cx["pauselinks"],"rdplinks":cx["rdplinks"],"rollbacklinks": cx["rollbacklinks"], "updatelinks": cx["updatelinks"],
    #                                             "removelinks": cx["removelinks"], "revisionslinks": cx["revisionslinks"],"statuslinks":cx["statuslinks"]
    #                                                 }))
    #             if cx["configName"].strip() == "":
    #                 cx.update({"configMap": "[]"})
    #                 cmapnew.append(ProjectService(**cx))
    #                 # print(cx["dpname"])
    #                 # cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
    #                 #                             "nsid": cx["nsid"], "nsname": cx["nsname"],
    #                 #                             "dpid": cx["dpid"], "dpname": cx["dpname"],
    #                 #                             "img": cx["img"], "replica": cx["replica"],
    #                 #                             "configName": cx["configName"],"configId": "","configMap":"",
    #                 #                             "pvcid": cx["pvcid"],
    #                 #                             "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"]})
    #                 # else:
    #                 #     cmapnew.append({"pjid": cx["pjid"], "pjname": cx["pjname"],
    #                 #                         "nsid": cx["nsid"], "nsname": cx["nsname"],
    #                 #                         "dpid": cx["dpid"], "dpname": cx["dpname"],
    #                 #                         "img": cx["img"], "replica": cx["replica"],
    #                 #                         "configName": cx["configName"],"configId": xxx["id"],"configMap":kvtmp,
    #                 #                         "pvcid": cx["pvcid"],
    #                 #                         "rancher_url":cx["rancher_url"],"pubsvc": cx["pubsvc"],})
    #                 # print(xxx["projectId"],cx["pjid"],xxx["name"],cx["configName"])
    #         print(len(cmapnew))
    #         try:
    #             ProjectService.objects.bulk_create(cmapnew)
    #         except Exception as e :
    #             print(e)

            # url = pvc.url
            # token = pvc.token
            # pvcnew = []
            # for px in cmapnew:
            #     kwargs = {
            #         "url": url.format(px["pjid"]),
            #         "headers": {"Authorization": token, "Content-Type": "application/json"}
            #     }
            #     res = RequestApiAgent().list(**kwargs)
            #     pvdatalist = (json.loads(res.content))["data"]
            #     for xxx in pvdatalist:
            #         if xxx["id"].strip() == px["pvcid"].strip():
            #             pvcnew.append(ProjectService(**{"top_project":px["top_project"],"toppjid":px["toppjid"],"pjid": px["pjid"], "pjname": px["pjname"],
            #                            "nsid": px["nsid"], "nsname": px["nsname"],
            #                            "dpid": px["dpid"], "dpname": px["dpname"],
            #                            "img": px["img"], "replica": px["replica"],"state":px["state"] ,
            #                            "configName": px["configName"], "configId": px["configId"],
            #                            "configMap": px["configMap"],
            #                            "pvcid": px["pvcid"],
            #                            "pvcsize": xxx.get("resources").get("requests").get("storage"),
            #                            "rancher_url": px["rancher_url"], "pubsvc": px["pubsvc"],
            #                            })local:p-wg946)
            #         else:
            #            pvcnew.append(ProjectService(**px))
                # if px["pvcid"] == "":
                #     pvcnew.append(ProjectService(**px))

            # print(len(pvcnew))
                # if px["pvcid"].strip() == "":
                #       pvcnew.append(ProjectService(**px))
                    # else:
                    #     pvcnew.append(ProjectService(**px))
            # try:
            #     ProjectService.objects.bulk_create(pvcnew)
            # except Exception as e :
            #     print(e)
            # print(pvcnew[:1])

            # def test_pb_approval(self):
                # a = ProjectService.objects.filter(pjname="ioc-platform").values('pjid').first()
                # a=ProjectService.objects.get(pjname='ioc-platform').
                # print(a)
            #     a = ProjectConfigMap.objects.filter(tag="ioc").values("id","pjid")
            #     for x in a:
            #         print(x)
                # a = ProjectConfigMap.objects.filter(tag='feiyan').values("id","pjid","configId").all()
                # for x in a:
                #     v = "https://rancher.feiyan.com/p/"+x['pjid']+'/config-maps/'+x['configId']
                #     # print(v)
                #     ProjectConfigMap.objects.filter(id=x['id']).update(verifyurl=v)
                    # print(x['id'])
                #--------------
                # pj = RancherApiConfig.objects.filter(env_id=4, label="GETPVC").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="ioc").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     if x['pjid'] == 'c-5tk6p:p-55knm':
                #         url = (pj.url).format(x['pjid'])
                #         kwargs = {
                #             "url": url,
                #             "headers": {"Authorization": token, "Content-Type": "application/json"}
                #         }
                #         res = RequestApiAgent().list(**kwargs)
                #         pjdatalist = (json.loads(res.content))["data"]
                #         for xx in pjdatalist:
                #             m = ProjectPvc.objects.create(
                #                 pjid=xx['projectId'],
                #                 nsname=xx['namespaceId'],
                #                 nsid=xx['namespaceId'],
                #                 pvcid=xx['id'],
                #                 pvcname=xx['name'],
                #                 storageid=xx['storageClassId'],
                #                 capacity=xx['status']['capacity']['storage'],
                #                 accessMode=xx['status']['accessModes'],
                #                 volumeid=xx['volumeId'],
                #                 dellinks=xx['links']['remove'],
                #                 selflinks=xx['links']['self'],
                #                 updatelinks=xx['links']['update'],
                #                 yamllinks=xx['links']['yaml'],
                #                 tag='ioc',
                #                 pjname='自动化发布',
                #             )
                #             m.save()
                #-------------------
                #spug test
                # pj = RancherApiConfig.objects.filter(env_id=4, label="GETCONFIGMAP").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="ioc").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     if x['pjid'] == 'c-5tk6p:p-55knm':
                #         url = (pj.url).format(x['pjid'])
                #         kwargs = {
                #             "url": url,
                #             "headers": {"Authorization": token, "Content-Type": "application/json"}
                #         }
                #         res = RequestApiAgent().list(**kwargs)
                #         pjdatalist = (json.loads(res.content))["data"]
                #         for xx in pjdatalist:
                #             t=[]
                #             for k, v in dict.items(xx["data"]):
                #                 t.append({"k":k,"v":v})
                #             m = ProjectConfigMap.objects.create(
                #                 pjid=xx['projectId'],
                #                 configId=xx['id'],
                #                 configName=xx['name'],
                #                 configMap=t,
                #                 nsname=xx['namespaceId'],
                #                 nsid=xx['namespaceId'],
                #                 dellinks=xx['links']['remove'],
                #                 selflinks=xx['links']['self'],
                #                 updatelinks=xx['links']['update'],
                #                 yamllinks=xx['links']['yaml'],
                #                 tag='ioc',
                #                 pjname='自动化发布'
                #             )
                #             m.save()
                #---------------------------------------------------------
                # get fangyi  configmap
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP",tag="feiyan").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="feiyan").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         t=[]
                #         for k, v in dict.items(xx["data"]):
                #             t.append({"k":k,"v":v})
                #         m = ProjectConfigMap.objects.create(
                #             pjid=xx['projectId'],
                #             configId=xx['id'],
                #             configName=xx['name'],
                #             configMap=t,
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='feiyan',
                #             verifyurl = "https://rancher.feiyan.com/p/" + xx["projectId"] + "/config-maps/" + xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()
                # #-------------------------------------------------------------
                # # get fangyi pvc
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPVC",tag="feiyan").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="feiyan").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         m = ProjectPvc.objects.create(
                #             pjid=xx['projectId'],
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             pvcid=xx['id'],
                #             pvcname=xx['name'],
                #             storageid=xx['storageClassId'],
                #             capacity=xx['status']['capacity']['storage'],
                #             accessMode=xx['status']['accessModes'],
                #             volumeid=xx['volumeId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='feiyan',
                #             verifyurl = "https://rancher.feiyan.com/p/" + xx["projectId"] + "/volumes/" + xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()
                #-------get fanyi uos configmap
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP",tag="feiyanuos").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="feiyan.uos").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         t=[]
                #         for k, v in dict.items(xx["data"]):
                #             t.append({"k":k,"v":v})
                #         m = ProjectConfigMap.objects.create(
                #             pjid=xx['projectId'],
                #             configId=xx['id'],
                #             configName=xx['name'],
                #             configMap=t,
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='feiyanuos',
                #             verifyurl = "https://rancher.feiyan.uos.com/p/" + xx["projectId"] + "/config-maps/" + xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()
                #-------------get  fanyi uos pvc
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPVC",tag="feiyanuos").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="feiyan.uos").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         m = ProjectPvc.objects.create(
                #             pjid=xx['projectId'],
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             pvcid=xx['id'],
                #             pvcname=xx['name'],
                #             storageid=xx['storageClassId'],
                #             capacity=xx['status']['capacity']['storage'],
                #             accessMode=xx['status']['accessModes'],
                #             volumeid=xx['volumeId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='feiyanuos',
                #             verifyurl = "https://rancher.feiyan.uos.com/p/" + xx["projectId"] + "/volumes/" + xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()
                #-------------------------------------------------------
                #get ioc pvc
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETPVC",tag="ioc").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="ioc").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         m = ProjectPvc.objects.create(
                #             pjid=xx['projectId'],
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             pvcid=xx['id'],
                #             pvcname=xx['name'],
                #             storageid=xx['storageClassId'],
                #             capacity=xx['status']['capacity']['storage'],
                #             accessMode=xx['status']['accessModes'],
                #             volumeid=xx['volumeId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='ioc',
                #             verifyurl = "https://rancher.ioc.com/p/" + xx["projectId"] + "/volumes/" + xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()
                # #---------------------------------------------------------------
                # # get  ioc configmap
                # pj = RancherApiConfig.objects.filter(env_id=2, label="GETCONFIGMAP",tag="ioc").first()
                # token = pj.token
                # a = ProjectService.objects.filter(rancher_url__contains="ioc").values("pjid").annotate(
                #     counts=Count("pjid"))
                # for x in a:
                #     url = (pj.url).format(x['pjid'])
                #     kwargs = {
                #         "url": url,
                #         "headers": {"Authorization": token, "Content-Type": "application/json"}
                #     }
                #     res = RequestApiAgent().list(**kwargs)
                #     pjdatalist = (json.loads(res.content))["data"]
                #     for xx in pjdatalist:
                #         t=[]
                #         for k, v in dict.items(xx["data"]):
                #             t.append({"k":k,"v":v})
                #         m = ProjectConfigMap.objects.create(
                #             pjid=xx['projectId'],
                #             configId=xx['id'],
                #             configName=xx['name'],
                #             configMap=t,
                #             nsname=xx['namespaceId'],
                #             nsid=xx['namespaceId'],
                #             dellinks=xx['links']['remove'],
                #             selflinks=xx['links']['self'],
                #             updatelinks=xx['links']['update'],
                #             yamllinks=xx['links']['yaml'],
                #             tag='ioc',
                #             verifyurl="https://rancher.ioc.com/p/"+xx["projectId"]+"/config-maps/"+xx['id'],
                #             pjname=(ProjectService.objects.filter(pjid=xx['projectId']).first()).pjname
                #         )
                #         m.save()

                #_----------------------------------------------------------
                    # print(pjdatalist)
                # for x in a:
                #     print(x['pjid'])
                # from django.db.models import Count
                # a = MultiDBUser.objects.annotate(num=Count('ipaddress'))
                # for x in a:
                #     print(x.ipaddress)
                # from openpyxl import load_workbook
                #
                # ws = load_workbook("/home/jin/文档/after.xlsx", read_only=True)['Sheet1']
                # for i, row in enumerate(ws.rows):
                #     if i == 0:  # 第1行是表头 略过
                #         continue

                    # if not DevicePositon.objects.filter(name=row[17].value).exists()  and  row[17].value is not None :
                    #      m = DevicePositon.objects.create(
                    #         name=(row[17].value).strip(),
                    #         created_by_id=1,
                    #      )
                    #      m.save()
                        # print(row[17].value)
                    # if not ProjectConfig.objects.filter(name=row[0].value).exists()  and  row[0].value is not None :
                    #     print(row[0].value)
                    # if not WorkZone.objects.filter(name=row[21].value).exists()  and  row[21].value is not None :
                    #      m = WorkZone.objects.create(
                    #         name=(row[21].value).strip(),
                    #         created_by_id=1,
                    #      )
                    #      m.save()
                    # if not Zone.objects.filter(name=row[10].value).exists()  and  row[10].value is not None :
                    #      m = Zone.objects.create(
                    #         name=row[10].value,
                    #         created_by_id=1,
                    #      )
                    #      m.save()
                    #     print(row[21].value)
                    # if not ConnctUser.objects.filter(name=row[7].value).exists() :
                    #     if row[7].value is not None  and row[7].value != ""  and row[7].value :
                    #         if row[7].value is None:
                    #             continue
                    #         else:
                    #              m = ConnctUser.objects.create(
                    #                 name=(row[7].value).strip(),
                    #                 created_by_id=1,
                    #              )
                    #              m.save()
                             # print(row[7].value)

                # from apps.config.models import ProjectConfig
                # a = ProjectConfig.objects.get(name='IOC事件管理与联动指挥系统')
                # print(a)
                # import ast
                # import operator
                # from functools import reduce
                # from django.db.models import Q
                # h = Host.objects.values("ipaddress","username").all()
                # for x in h:
                #     print(ConnctUser.objects.get(pk=x["username"]).name)
                # Host.objects.filter(reduce())
                # a = Host.objects.filter(zone__in=[1,2,3])
                # print(a)
                # from openpyxl import load_workbook
                # ws = load_workbook("/home/jin/文档/root.xlsx", read_only=True)['Sheet1']
                # for i, row in enumerate(ws.rows):
                #     Host.objects.filter(ipaddress=row[0].value).update(password_hash=Host.make_password(row[1].value))
                    # print(row[0].value,row[1].value)
                # from apps.host.models import ConnctUser
                # u = Host.objects.get(ipaddress='192.168.1.107')
                # print((ConnctUser.objects.get(name='ioc')).id)
                # ioc = []
                # u = Host.objects.get(id=243)
                # u.status = 1
                # ioc.append(u)
                # ioc.append(Host(id=243,status=1))
                # Host.objects.bulk_update(ioc,['status'])
                # h = Host.objects.values("ipaddress","username","id").all()
                # print(u.name)
                # ipioc=[]
                # iproot = []
                # for x in h:
                #     if x['username'] == 'ioc':
                #         ipioc.append(x['ipaddress'])
                #     if x['username'] == 'root':
                #         iproot.append(x['ipaddress'])
                # import subprocess
                # subp = subprocess.Popen("ls /home/jin/下载/bag/ioc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                #                         encoding="utf-8")
                # a =subp.communicate()
                # b = list(a)[0]
                # c = b.split("\n")
                # print(c)
                # for x in c:
                #     print(x)
                # print(c)
                # print(b)
                # c = ",".join(b)
                # print(c)
                # for x in a.readlines():
                #     print(x)
                # from apps.host.models import Host
                # from libs.pwd import  decryptPwd
                # a = Host.objects.filter(ostp="Windows").values("password_hash")
                # for x in a:
                #     if x["password_hash"]:
                #         print(x['password_hash'])
                #         print(decryptPwd(x['password_hash']))
                        # print(bytes(x['password_hash'],encoding='utf8'))
                      # print(Host.plaxt_password(x["password_hash"]))
                # from apps.account.models import User
                # a = User.objects.all().values("email")
                # print(a)
                # x = ProjectServiceApprovalNotice.objects.filter(service_id=1).values("notice_user__email").all()
                # a = []
                # for b in x:
                #    a.append(b["notice_user__email"])
                # print(",".join(a))
                # print(ProjectServiceApprovalNotice.objects.filter(service_id=1).first())
                # for x in a:
                #     print(x.state)
                #    print(x.to_dict())

                # from apps.message.models import EmailRecord
                # message = EmailRecord.objects.create(
                #     to_email="13113252872@126.com",
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     subject="aaa",
                #     content="aaa",
                # )
                # if not isinstance(message, EmailRecord):
                #     print("aaaa")
                #     return
                # print(message.to_email)
                # try:
                #     r = send_mail('易百商城邮箱验证', '易百商城邮箱验证', settings.DEFAULT_FROM_EMAIL,
                #                   ["13113252872@126.com"] )
                #     print(r)
                #
                # except Exception as e :
                #     print(e)
                # from apps.app.models import App
                # m = App.objects.create(name='aaa', key='aaaadd',created_by_id=1)
                # m.save()
                # print(m.id)
                # ob = ProjectServiceApprovalNotice.objects.all()
                # for x in ob.values('service__top_project').distinct():
                #     print(x)
                # m1 = ProjectServiceApproval.objects.create(
                #     service_id=1,
                #     pbtype=1,
                #     opshandler='test',
                #     opsstatus=1,
                #     dbhandler='test',
                #     dbstatus=1,
                #     leaderhandler='test',
                #     leaderstatus=1
                # )
                # m1.save()
    # def test_ioc_nodes(self):
    #     d = RancherApiConfig.objects.filter(env_id=3,label="NODES").first()
    #     url = d.url
    #     token = d.token
    #     kwargs = {
    #         "url": url,
    #         "headers": {"Authorization": token, "Content-Type": "application/json"}
    #     }
    #     res = RequestApiAgent().list(**kwargs)
    #     pjdatalist = (json.loads(res.content))["data"]
    #     for x in pjdatalist:
    #         m = RancherNode.objects.create(
    #             state=x['state'],
    #             ipaddress=x['ipAddress'],
    #             nodeid=x['id'],
    #             clusterid=x['clusterId'],
    #             worker=x['worker'],
    #             create_by_id=1,
    #             hostname=x['hostname'],
    #             tag="feiyan"
    #         )
    #         m.save()

    def test(self):
    #     kwargs = {
    #         # "url": "https://rancher.ioc.com/v3/project/c-5tk6p:p-55knm/workloads/deployment:spug:test1234/revisions",
    #         "url": "https://rancher.ioc.com/v3/project/c-5tk6p:p-55knm/workloads/deployment:spug:testcmap",
    #         "headers": {"Authorization": 'Bearer token-s6mvd:vqf7qjrktx8fdlwq28z9bb94mxwgg55t7ssd645qhxjlb47blx9xc2', "Content-Type": "application/json"},
    #         # "data": json.dumps({
    #         #     "type":"configMap",
    #         #     "data":{"a": "666"},
    #         #     "labels":{},
    #         #     "id": "spug:spugtest",
    #         #     "namespaceId": "spug"
    #         # })
    #     }
        # res = RequestApiAgent().list(**kwargs)
        # # print(res)
        # list = json.loads(res.content)
        # print(list)
        # print(json.dumps(list))
        # a = RancherSvcPubStandby.objects.get(id=40)
        # data = {}
        # for x in ast.literal_eval(a.configMap):
        #     data[x["k"]] =x["v"]
        # print(data)
        # t = Host.objects.values("top_project", "child_project").all()
        # for x in t:
        #     for xx in ast.literal_eval(x['top_project']):
        #         print(type(xx))

        return




