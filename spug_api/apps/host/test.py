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
        iplist = ["10.145.188.134", "10.147.3.65", " 19.104.40.35", " 19.104.48.33", " 19.104.50.124", "19.104.50.60",
         " 19.104.53.124", "19.104.53.219", "19.106.85.10", "19.106.85.26", "19.106.85.68", "10.145.188.135",
         "10.147.3.66", " 19.104.40.36", " 19.104.49.142", "19.104.50.125", "19.104.50.72", " 19.104.53.126",
         "19.104.53.48", " 19.106.85.11", "19.106.85.27", "19.106.85.69", "10.146.0.53", " 10.147.3.67",
         " 19.104.40.37", " 19.104.49.143", "19.104.50.131", "19.104.50.73", " 19.104.53.129", "19.104.53.53",
         " 19.106.85.12", "19.106.85.28", "19.106.85.7", "10.147.1.128", "10.147.3.68", " 19.104.40.38",
         " 19.104.49.144", "19.104.50.139", "19.104.50.74", " 19.104.53.130", "19.104.53.54", " 19.106.85.13",
         "19.106.85.29", "19.106.85.70", "10.147.1.129", "10.147.4.247", "19.104.40.40", " 19.104.49.145",
         "19.104.50.141", "19.104.50.75", " 19.104.53.131", "19.104.53.55", " 19.106.85.14", "19.106.85.3",
         " 19.106.85.72", "10.147.1.130", "19.104.40.14", "19.104.40.46", " 19.104.49.146", "19.104.50.142",
         "19.104.50.76", " 19.104.53.132", "19.104.53.56", " 19.106.85.15", "19.106.85.30", "19.106.85.73",
         "10.147.2.49", " 19.104.40.15", "19.104.40.8", "19.104.49.147", "19.104.50.155", "19.104.50.77",
         " 19.104.53.133", "19.104.53.57", " 19.106.85.16", "19.106.85.31", "19.106.85.74", "10.147.2.50",
         " 19.104.40.19", "19.104.40.9", "19.104.49.148", "19.104.50.160", "19.104.50.86", " 19.104.53.134",
         "19.104.53.58", " 19.106.85.17", "19.106.85.32", "19.106.85.8", "10.147.2.51", " 19.104.40.21",
         "19.104.44.194", "19.104.49.149", "19.104.50.181", "19.104.51.125", "19.104.53.135", "19.104.53.59",
         " 19.106.85.18", "19.106.85.33", "19.106.85.9", "10.147.2.52", " 19.104.40.23", "19.104.44.195",
         "19.104.49.150", "19.104.50.188", "19.104.51.126", "19.104.53.136", "19.104.53.60", " 19.106.85.19",
         "19.106.85.34", "10.147.2.58", " 19.104.40.24", "19.104.44.196", "19.104.49.151", "19.104.50.195",
         "19.104.51.127", "19.104.53.137", "19.104.53.61", " 19.106.85.2", " 19.106.85.35", "10.147.3.246",
         "19.104.40.29", "19.104.44.197", "19.104.50.1", "19.104.50.204", "19.104.51.128", "19.104.53.138",
         "19.104.53.62", " 19.106.85.20", "19.106.85.36", "10.147.3.60", " 19.104.40.30", "19.104.44.198",
         "19.104.50.109", "19.104.50.210", "19.104.51.129", "19.104.53.213", "19.104.53.63", " 19.106.85.21",
         "19.106.85.37", "10.147.3.61", " 19.104.40.31", "19.104.44.199", "19.104.50.11", " 19.104.50.219",
         "19.104.51.149", "19.104.53.214", "19.104.53.64", " 19.106.85.22", "19.106.85.38", "10.147.3.62",
         " 19.104.40.32", "19.104.48.30", " 19.104.50.116", "19.104.50.227", "19.104.52.95", " 19.104.53.215",
         "19.104.59.1", "19.106.85.23", "19.106.85.4", "10.147.3.63", " 19.104.40.33", "19.104.48.31", " 19.104.50.118",
         "19.104.50.43", " 19.104.53.122", "19.104.53.216", "19.104.59.2", "19.106.85.24", "19.106.85.5", "10.147.3.64",
         " 19.104.40.34", "19.104.48.32", " 19.104.50.121", "19.104.50.55", " 19.104.53.123", "19.104.53.217",
         "19.104.59.3", "19.106.85.25", "19.106.85.6"]
        for x in iplist:
            try:
                with open("/home/jin/cmdbv3/spug/spug_api/out/"+x.strip()) as f:
                # with open("/home/jin/cmdbv3/spug/spug_api/out/" + "19.104.51.129") as f:
                    a = f.read()
                    ser = json.loads(a)
                    ttmp = []
                # print(ser["ansible_facts"]["ansible_mounts"])
                    # for x in ser["ansible_facts"]["ansible_mounts"]:
                    #     print(x["size_total"])
                    for xx in ser["ansible_facts"]["ansible_mounts"]:
                        # print(xx)
                        if not xx["mount"].startswith(('/var','/boot','/home','/media','/usr','/tmp','/mnt')):
                            # if xx["mount"] != "/":
                                ttmp.append({"type":xx["fstype"],"name": xx["device"],"mount":xx["mount"],"total_szie":math.ceil(xx.get("size_total",0) / 1024 /1024/1024),"used": math.ceil((xx.get("size_total",0) - xx.get("block_total",0) - xx.get("size_available",0)) / 1024/1024/1024) })
                                # ttmp.append({"type":xx["fstype"],"name": xx["device"],"mount":xx["mount"], "total_szie":math.ceil(xx.get("size_total",0) / 1024 /1024/1024)})


                    t=[x for x in ser["ansible_facts"]["ansible_all_ipv4_addresses"]
                       if not x.startswith(("172.17","172.17","172.18","172.19","172.20","172.21","172.23","172.22","172.27","172.24","172.26","172.27",
                                            "172.28","172.29","172.30","192.168","10.42","10.128","10.129","10.130")) ]
                    tip=""
                    if len(t) >1 and ser["ansible_facts"].get("ansible_bond1"):
                        tip =ser["ansible_facts"]["ansible_bond1"]["ipv4"]["address"]
                    elif len(t) == 1:
                        tip = t[0]
                    elif len(t)> 1 and ser["ansible_facts"].get("ansible_default_ipv4"):
                        tip = ser["ansible_facts"]["ansible_default_ipv4"]["address"]

                Host.objects.create(
                        # ipaddress=[ x  for x in ser["ansible_facts"]["ansible_all_ipv4_addresses"] if not x.startswith("192.168") ][0],
                        ipaddress=tip,
                        osType=ser["ansible_facts"]["ansible_distribution"],
                        osVerion=ser["ansible_facts"]["ansible_distribution_version"],
                        coreVerion=ser["ansible_facts"]["ansible_kernel"],
                        # disk=[{"type": x["fstype"],"name":x["device"],"mount":x["mount"],"size": math.ceil(x.get("size_total",0) / 1024 /1024/1024) }  for x in ser["ansible_facts"]["ansible_mounts"]],
                        disk=ttmp,
                        disks=len(ser["ansible_facts"]["ansible_mounts"]),
                        # memory= int(ser["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
                        memory=math.ceil(ser["ansible_facts"]["ansible_memtotal_mb"] / 1024 ),
                        cpus=int(ser["ansible_facts"]["ansible_processor_count"]) * int(ser["ansible_facts"]["ansible_processor_cores"]) ,
                        # cpucore=ser["ansible_facts"]["ansible_processor_cores"],
                        hostname=ser["ansible_facts"]["ansible_nodename"],
                        supplier=ser["ansible_facts"]["ansible_system_vendor"],
                        port=22,
                        username="root",
                        ostp=0,
                        env_id=2,

                    )
            except Exception as e:
                print(e,x)
                print((json.loads(a))["ansible_facts"]["ansible_all_ipv4_addresses"])

        # print(ttmp)