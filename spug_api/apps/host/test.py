from libs.utils import RequestApiAgent
from django.conf import settings
import json
from apps.app.models import RancherNamespace, RancherConfigMap, RancherProject, RancherDeployment, RancherSvcPubStandby
from apps.config.models import RancherApiConfig
from apps.host.models import  Host
import unittest
import ast


class Mytest(unittest.TestCase):
    # def test_get_disk(self):
    #     data = Host.objects.values("id","disk")
    #     disks = list(data)
    #     # print(disks)
    #     newtmp = []
    #     for x in disks:
    #         if x.get("disk"):
    #             tmp =ast.literal_eval(x.get('disk'))
    #             # print(tmp)
    #             for xx in tmp:
    #                 if not xx["mount"].startswith(('/var','/boot','/home','/media','/usr','/tmp','/mnt')):
    #                    if  xx["mount"] != "/":
                            # newtmp.append(xx)
                            # break
                    # print(xx)aaaaaaaaa
                # print(x.get('disk'))
                # print(type(ast.literal_eval(x.get('disk'))))
                # for x in a :
                #     print(x)
                # a = (json.dumps(x.get('disk'))).split('"')[1]
                # print(a)
                # print(type(list(a)))
                # break
        # print(newtmp)

        # a = list(set(newtmp))
        # for x in a:
        #     print(x)
    def test(self):
        from apps.host.models import Host
        import math
        import subprocess
        subp = subprocess.Popen("ls /home/jin/cmdbv3/spug/spug_api/out/root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding="utf-8")
        a = subp.communicate()
        b = list(a)[0]
        iplist = b.split("\n")
        # global tag
        from apps.host.models import Datadisk
        import ast
        bb = Datadisk.objects.values("disk")
        cc = list(bb)
        tag = []
        for x in cc:
            tag = ast.literal_eval(x["disk"])
        for x in iplist:
            if  x != "":
                try:
                    with open("/home/jin/cmdbv3/spug/spug_api/out/root/"+x.strip()) as f:
                    # with open("/home/jin/cmdbv3/spug/spug_api/out/" + "19.104.51.129") as f:
                        a = f.read()
                        ser = json.loads(a)
                        # ttmp = []
                    # print(ser["ansible_facts"]["ansible_mounts"])
                        # for x in ser["ansible_facts"]["ansible_mounts"]:
                        #     print(x["size_total"])
                        # for xx in ser["ansible_facts"]["ansible_mounts"]:
                        #     # print(xx)
                        #     if not xx["mount"].startswith(('/var','/boot','/home','/media','/usr','/tmp','/mnt')):
                        #         # if xx["mount"] != "/":
                        #             ttmp.append({"type":xx["fstype"],"name": xx["device"],"mount":xx["mount"],"total_szie":math.ceil(xx.get("size_total",0) / 1024 /1024/1024),"used": math.ceil((xx.get("size_total",0) - xx.get("block_total",0) - xx.get("size_available",0)) / 1024/1024/1024) })
                        #             # ttmp.append({"type":xx["fstype"],"name": xx["device"],"mount":xx["mount"], "total_szie":math.ceil(xx.get("size_total",0) / 1024 /1024/1024)})
                        ttmp = [{"type":xx["fstype"],"name": xx["device"],"mount":xx["mount"],"total_size":math.ceil(xx.get("size_total",0) / 1024 /1024/1024),
                                 "used": math.ceil((xx.get("size_total",0) - xx.get("block_total",0) - xx.get("size_available",0)) / 1024/1024/1024)}
                                 for xx in ser["ansible_facts"]["ansible_mounts"] if not xx["mount"].startswith(('/var','/boot','/home','/media','/usr','/tmp','/mnt','/recovery'))]
                        t=[x for x in ser["ansible_facts"]["ansible_all_ipv4_addresses"]
                           if not x.startswith(("172.17","172.18","172.19","172.20","172.21","172.23","172.22","172.27","172.24","172.26","172.27",
                                                "172.28","172.29","172.30","192.168","10.42","10.128","10.129","10.130"))  ]

                        # for d in ttmp:
                        #     if d["mount"] != "/":
                        #         tag.append(d["mount"])
                                # tag.append({"m": d["mount"], "s": d["total_size"], "d": d["name"]})
                        # tag = [x["mount"] for x in ttmp if x["mount"] != "/"]
                        tip=""
                        if len(t) >1 and ser["ansible_facts"].get("ansible_bond1"):
                            tip =ser["ansible_facts"]["ansible_bond1"]["ipv4"]["address"]
                        elif len(t) == 1:
                            tip = t[0]
                        elif len(t)> 1 and ser["ansible_facts"].get("ansible_default_ipv4"):
                            tip = ser["ansible_facts"]["ansible_default_ipv4"]["address"]

                        sysdisk = [x for x in ttmp  if x["mount"] =="/" ]
                        # keyworkds = "/data,/opt"
                        # datadisk = [w in tag and w for w in keyworkds.split(',')]
                        datadisk = [ {"name":x["name"] ,"size": x["total_size"],"mount":x["mount"]} for x in ttmp if x["mount"] != "/" and x["mount"] in tag]
                    Host.objects.create(
                            # ipaddress=[ x  for x in ser["ansible_facts"]["ansible_all_ipv4_addresses"] if not x.startswith("192.168") ][0],
                            ipaddress=tip,
                            osType=ser["ansible_facts"].get("ansible_distribution","Centos"),
                            osVerion=ser["ansible_facts"].get("ansible_distribution_version",None),
                            coreVerion=ser["ansible_facts"]["ansible_kernel"],
                            # disk=[{"type": x["fstype"],"name":x["device"],"mount":x["mount"],"size": math.ceil(x.get("size_total",0) / 1024 /1024/1024) }  for x in ser["ansible_facts"]["ansible_mounts"]],
                            disk=ttmp,
                            disks=len(ser["ansible_facts"]["ansible_mounts"]),
                            # memory= int(ser["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
                            # memory=math.ceil(ser["ansible_facts"]["ansible_memtotal_mb"] / 1024 ),
                            memory=round(ser["ansible_facts"]["ansible_memtotal_mb"] / 1024 ,2),
                            cpus=int(ser["ansible_facts"]["ansible_processor_count"]) * int(ser["ansible_facts"]["ansible_processor_cores"]) ,
                            # cpucore=ser["ansible_facts"]["ansible_processor_cores"],
                            hostname=ser["ansible_facts"]["ansible_nodename"],
                            supplier=ser["ansible_facts"]["ansible_system_vendor"],
                            port=22,
                            username="1",
                            ostp="Linux",
                            env_id=2,
                            resource_type="2",
                            sys_disk= sysdisk,
                            data_disk= datadisk,
                            # data_disk=set(list(tag)),
                        )
                except Exception as e:
                    print(e,x)
                    print((json.loads(a))["ansible_facts"]["ansible_all_ipv4_addresses"])

        # from apps.host.models import Datadisk
        # for x in tag:
        #     print(x)
        # import ast

        # a  = Datadisk.objects.create(disk=list(set(tag)))
        # a.save()
        # b = Datadisk.objects.values("disk")
        # c = list(b)
        # for x in c:
        #     d = ast.literal_eval(x["disk"])
        # for  xx in d:
        #     print(xx)
        # print(list(set(tag)))