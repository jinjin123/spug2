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
    for xip in ip:
        if stdout_dict['success'].get(xip):
            try:
                data = dict(
                    ipaddress=[x for x in stdout_dict['success'][xip]["ansible_facts"]["ansible_all_ipv4_addresses"] if
                               not x.startswith(("172."))][0],
                    # paddress=[ x  for x in stdout_dict['success'][xip]["ansible_facts"]["ansible_all_xipv4_addresses"] ][0],
                    osType=stdout_dict['success'][xip]["ansible_facts"]["ansible_distribution"],
                    osVerion=stdout_dict['success'][xip]["ansible_facts"]["ansible_distribution_version"],
                    coreVerion=stdout_dict['success'][xip]["ansible_facts"]["ansible_kernel"],
                    disk=[{"type": x["fstype"], "name": x["device"], "mount": x["mount"],
                           "size": math.ceil(x.get("size_total", 0) / 1024 / 1024 / 1024)} for x in
                          stdout_dict['success'][xip]["ansible_facts"]["ansible_mounts"]],
                    disks=len(stdout_dict['success'][xip]["ansible_facts"]["ansible_mounts"]),
                    status="Y",
                    # memory= int(stdout_dict['success'][xip]["ansible_facts"]["ansible_memory_mb"]["real"]["total"] / 1024 ),
                    memory=math.ceil(stdout_dict['success'][xip]["ansible_facts"]["ansible_memtotal_mb"] / 1024),
                    cpus=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_count"],
                    cpucore=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_cores"],
                    hostname=stdout_dict['success'][xip]["ansible_facts"]["ansible_nodename"],
                    supplier=stdout_dict['success'][xip]["ansible_facts"]["ansible_system_vendor"]
                )
                Host.objects.update_or_create(defaults=data,ipaddress=xip,status="Y")
            except Exception as e:
                print(e)
                logger.error("update host %s error :%s",(xip,e))
        else:
            print('no')
            logger.error("host %s connect failed" , xip)
