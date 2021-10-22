from spug.celery import app
from libs.ansible29 import *
from apps.host.models import Host,Datadisk
import ast
import math
import logging
logger = logging.getLogger('spug_log')
@app.task
def update_hostinfo(ip,user='root'):
    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user=user)  # 创建资源库对象
    ansible3.run(hosts=ip, module="setup", args='')
    stdout_dict = json.loads(ansible3.get_result())
    bb = Datadisk.objects.values("disk")
    cc = list(bb)
    tag = []
    for x in cc:
        tag = ast.literal_eval(x["disk"])
    for xip in ip:
        if stdout_dict['success'].get(xip):
            try:
                ttmp = [{"type": xx["fstype"], "name": xx["device"], "mount": xx["mount"],
                         "total_size": math.ceil(xx.get("size_total", 0) / 1024 / 1024 / 1024),
                         "used": math.ceil((xx.get("size_total", 0) - xx.get("block_total", 0) - xx.get(
                             "size_available", 0)) / 1024 / 1024 / 1024)}
                        for xx in stdout_dict['success'][xip]["ansible_facts"]["ansible_mounts"] if not xx["mount"].startswith(
                        ('/var', '/boot', '/home', '/media', '/usr', '/tmp', '/mnt', '/recovery'))]

                t = [x for x in stdout_dict['success'][xip]["ansible_facts"]["ansible_all_ipv4_addresses"]
                     if not x.startswith((
                                         "172.17", "172.18", "172.19", "172.20", "172.21", "172.23", "172.22", "172.27",
                                         "172.24", "172.26", "172.27",
                                         "172.28", "172.29", "172.30", "192.168", "10.42", "10.128", "10.129",
                                         "10.130"))]
                tip = ""
                if len(t) > 1 and stdout_dict['success'][xip]["ansible_facts"].get("ansible_bond1"):
                    tip = stdout_dict['success'][xip]["ansible_facts"]["ansible_bond1"]["ipv4"]["address"]
                elif len(t) == 1:
                    tip = t[0]
                elif len(t) > 1 and stdout_dict['success'][xip]["ansible_facts"].get("ansible_default_ipv4"):
                    tip = stdout_dict['success'][xip]["ansible_facts"]["ansible_default_ipv4"]["address"]

                sysdisk = [x for x in ttmp if x["mount"] == "/"]
                datadisk = [{"name": x["name"], "size": x["total_size"], "mount": x["mount"]} for x in ttmp if
                            x["mount"] != "/" and x["mount"] in tag]

                data = dict(
                    ipaddress=tip,
                    # paddress=[ x  for x in stdout_dict['success'][xip]["ansible_facts"]["ansible_all_xipv4_addresses"] ][0],
                    osType=stdout_dict['success'][xip]["ansible_facts"].get("ansible_distribution","Centos"),
                    osVerion=stdout_dict['success'][xip]["ansible_facts"].get("ansible_distribution_version","7.6"),
                    coreVerion=stdout_dict['success'][xip]["ansible_facts"]["ansible_kernel"],
                    disk=ttmp,
                    disks=len(stdout_dict['success'][xip]["ansible_facts"]["ansible_mounts"]),
                    status=0,
                    # memory= int(stdout_dict['success'][xip]["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
                    # memory=math.ceil(stdout_dict['success'][xip]["ansible_facts"]["ansible_memtotal_mb"] / 1024),
                    memory=round(stdout_dict['success'][xip]["ansible_facts"]["ansible_memtotal_mb"] / 1024, 2),

                    # cpus=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_count"],
                    # cpucore=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_cores"],
                    cpus=int(stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_count"]) * int(stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_cores"]),

                    hostname=stdout_dict['success'][xip]["ansible_facts"]["ansible_nodename"],
                    supplier=stdout_dict['success'][xip]["ansible_facts"]["ansible_system_vendor"],
                    username=user,
                    port=22,
                    ostp="Linux",
                    env_id=2,
                    resource_type="主机",
                    sys_disk=sysdisk,
                    data_disk=datadisk,
                )
                Host.objects.update_or_create(defaults=data,ipaddress=xip,status=0)
            except Exception as e:
                print(e)
                logger.error("update host %s error :%s",(xip,e))
        else:
            print('no')
            logger.error("host %s connect failed" , xip)
