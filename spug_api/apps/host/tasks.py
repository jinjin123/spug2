from spug.celery import app
from libs.ansible29 import *
from apps.host.models import Host
import math
import logging
logger = logging.getLogger('spug_log')
@app.task
def update_hostinfo(ip,user='root'):
    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user=user)  # 创建资源库对象
    ansible3.run(hosts=ip, module="setup", args='')
    stdout_dict = json.loads(ansible3.get_result())
    # print(stdout_dict)
    if stdout_dict['success'].get(ip):
        try:
            Host.objects.filter(ipaddress=ip).update(
                ipaddress=[ x  for x in stdout_dict['success'][ip]["ansible_facts"]["ansible_all_ipv4_addresses"] if not x.startswith(("192.168","172.23","172.18")) ][0],
                # ipaddress=[ x  for x in stdout_dict['success'][ip]["ansible_facts"]["ansible_all_ipv4_addresses"] ][0],
                osType=stdout_dict['success'][ip]["ansible_facts"]["ansible_distribution"],
                osVerion=stdout_dict['success'][ip]["ansible_facts"]["ansible_distribution_version"],
                coreVerion=stdout_dict['success'][ip]["ansible_facts"]["ansible_kernel"],
                disk=[{"type": x["fstype"],"name":x["device"],"mount":x["mount"],"size": math.ceil(x.get("size_total",0) / 1024 /1024/1024) }  for x in stdout_dict['success'][ip]["ansible_facts"]["ansible_mounts"]],
                disks=len(stdout_dict['success'][ip]["ansible_facts"]["ansible_mounts"]),
                status="Y",
                # memory= int(stdout_dict['success'][ip]["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
                memory=math.ceil(stdout_dict['success'][ip]["ansible_facts"]["ansible_memtotal_mb"] / 1024 ),
                cpus=stdout_dict['success'][ip]["ansible_facts"]["ansible_processor_count"],
                cpucore=stdout_dict['success'][ip]["ansible_facts"]["ansible_processor_cores"],
                hostname=stdout_dict['success'][ip]["ansible_facts"]["ansible_nodename"],
                supplier=stdout_dict['success'][ip]["ansible_facts"]["ansible_system_vendor"],
            )
        except Exception as e:
            logger.error("update host %s error :%s",(ip,e))
    else:
        logger.error("host %s connect failed" , ip)
