from spug.celery import app
from libs.ansible29 import *
from apps.host.models import *
from libs.utils import randpass,RequestApiAgent
from apps.message.tasklog import tasksave
from django.db.models import Count
from django.core.cache import cache
import ast
import math
import logging
import socket
import time
import re
import traceback
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
                sys_size = [int(x["total_size"]) for x in sysdisk][0]
                data_size = 0
                sysdatasize = ""
                if len(datadisk) > 0:
                    for x in datadisk:
                        data_size += int(x["size"])
                if data_size != 0:
                    sysdatasize = (str(sys_size) + "G") + "+" + (str(data_size) + "G")
                else:
                    sysdatasize = str(sys_size) + "G"
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
                    memory=math.ceil(stdout_dict['success'][xip]["ansible_facts"]["ansible_memtotal_mb"] / 1024),
                    # memory=round(stdout_dict['success'][xip]["ansible_facts"]["ansible_memtotal_mb"] / 1024, 2),

                    # cpus=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_count"],
                    # cpucore=stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_cores"],
                    cpus=int(stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_count"]) * int(stdout_dict['success'][xip]["ansible_facts"]["ansible_processor_cores"]),

                    hostname=stdout_dict['success'][xip]["ansible_facts"]["ansible_nodename"],
                    supplier=stdout_dict['success'][xip]["ansible_facts"]["ansible_system_vendor"],
                    username=(ConnctUser.objects.get(name=user)).id,
                    # port=22,
                    # ostp="Linux",
                    # env_id=2,
                    # resource_type="主机",
                    sys_disk=sysdisk,
                    data_disk=datadisk,
                    sys_data=sysdatasize,
                )
                # ip + user filter one
                Host.objects.update_or_create(defaults=data,ipaddress=xip,username=(ConnctUser.objects.get(name=user)).id)
                # Host.objects.filter(ipaddress=xip).update(**data)
                cache.delete("host_all")
            except Exception as e:
                print(e)
                logger.error(msg="update host %s error :%s"%(xip,e))
        else:
            print('no')
            logger.error(msg="host %s connect failed" % (xip))


@app.task
def update_hoststatus():
    h = Host.objects.values("ipaddress", "username").all()
    ipioc = []
    iproot = []
    for x in h:
        if x['username'] == 'ioc':
            ipioc.append(x['ipaddress'])
        if x['username'] == 'root':
            iproot.append(x['ipaddress'])

    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='ioc')
    ansible3.run(hosts=ipioc, module="ping", args='')
    stdout_dict = json.loads(ansible3.get_result())
    ioc_batch =[]
    root_batch =[]
    for xx in ipioc:
        if not stdout_dict['success'].get(xx):
            ioc_batch.append(Host(id=(Host.objects.get(ipaddress=xx)).id,status=1))

    Host.objects.bulk_update(ioc_batch,['status'])
    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='root')
    ansible3.run(hosts=iproot, module="ping", args='')
    stdout_dict = json.loads(ansible3.get_result())

    for xxx in iproot:
        if not stdout_dict['success'].get(xxx):
            root_batch.append(Host(id=(Host.objects.get(ipaddress=xxx)).id, status=1))
    Host.objects.bulk_update(root_batch,['status'])


@app.task
def update_pwd(ip, user):
    ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user=user)  # 创建资源库对象
    m = randpass()
    global stdout_dict
    try:
        ansible3.run(hosts=ip, module="user", args="name=%s update_password=always password={{ '%s'|password_hash('sha512') }} "%(user,m))
        stdout_dict = json.loads(ansible3.get_result())
        if stdout_dict["success"].get(ip):
            Host.objects.filter(ipaddress=ip).update(password_hash=Host.make_password(m))
            tasksave('update_pwd',stdout_dict,0)
            logger.info(msg="##update password## ->ip:%s,user:%s ,pwd:%s"%(ip,user,m))
        else:
            logger.error(msg="##update password faild## ->ip:%s,user:%s ,pwd:%s"%(ip,user,m))

    except Exception as e:
        logger.error(msg="##update password faild##"+ str(e))
        tasksave('update_pwd', stdout_dict, 1)


@app.task
def check_db_port():
    try:
        hosts = Host.objects.filter(resource_type=(ResourceType.objects.get(name='数据库')).id).values("ipaddress", "port").all().exclude(ipaddress="")
        for x in hosts:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            d = s.connect_ex((x['ipaddress'],x['port']))
            if d == 0:
                Host.objects.filter(resource_type=(ResourceType.objects.get(name='数据库')).id,ipaddress=x['ipaddress'],port=x['port']).update(status=0)
            else:
                Host.objects.filter(resource_type=(ResourceType.objects.get(name='数据库')).id,ipaddress=x['ipaddress'],port=x['port']).update(status=1)
    except:
        pass

@app.task
def check_system_url():
    urlobj = SystemCheck.objects.values('name','url').filter(status__isnull=True).all()
    for x in urlobj:
          kwargs = {
               "url": "",
               "headers": {"Content-Type": "application/json"}
          }
          kwargs['url'] = x['url']
          try:
               res = RequestApiAgent().list(**kwargs)
               if res.status_code == 200:
                    SystemCheck.objects.create(name=x['name'],url=x['url'],check_time=time.localtime(),status=0)
               else:
                    SystemCheck.objects.create(name=x['name'],url=x['url'],check_time=time.localtime(),status=1)
          except Exception as e :
              # SystemCheck.objects.create(name=x['name'], url=x['url'], check_time=time.localtime(), status=1)
              logger.error(msg="check  health url faild ---->"+ x['url'] + str(e))



@app.task
def check_system_hard():
    hosts = Host.objects.filter(resource_type=(ResourceType.objects.get(name='主机')).id, ostp='Linux').all().exclude(
        ipaddress="")
    logger.info(msg="------ scan host health start -----------")
    for x in hosts:
        ips = x.ipaddress
        try:
            if (ConnctUser.objects.filter(id=x.username).values('name').first())['name'] == 'ioc':
                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='ioc')
                ansible3.run(hosts=ips, module="shell",args="top -bn1 | grep load | awk '{printf $(NF-2)}'|awk -F ',' '{print $1}' ")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    cus = Host.objects.filter(resource_type=(ResourceType.objects.get(name='主机')).id,ostp='Linux',ipaddress=ips).values('cpus').exclude(ipaddress="").first()['cpus']
                    if cus is not None:
                        cpubl = (int(float(stdout_dict['success'][ips]['stdout']) * 100 / cus))
                        SystemHealthInfo.objects.create(ipaddress=ips,
                                                            cpublance=cpubl,
                                                            cpus=cus,
                                                            check_time=time.localtime())
                    else:
                        cpubl = 100
                        SystemHealthInfo.objects.create(ipaddress=ips,
                                                        cpublance=100,
                                                        cpus=cus,
                                                        check_time=time.localtime())
                    if cpubl > 85:
                        SystemHealthInfo.objects.filter(ipaddress=ips, check_time=time.localtime()).update(status=2)
                    else:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=0)
                else:
                    SystemHealthInfo.objects.create(ipaddress=ips, status=1,check_time=time.localtime())

                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='ioc')
                ansible3.run(hosts=ips, module="shell",args="df -h  | grep -vE '^Filesystem|tmpfs|cdrom|overlay|boot|loop|shm' | awk 'NR>1{print}'")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    dsinfo = stdout_dict['success'][ips]['stdout']
                    matchlist = re.findall("\d+%", dsinfo)
                    for x in matchlist:
                        if int(x.split("%")[0]) > 70 and int(x.split("%")[0]) < 85:
                            SystemHealthInfo.objects.filter(ipaddress=ips, check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=2,status=2)
                        elif int(x.split("%")[0]) > 85:
                            SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=1,status=1)
                            break
                        else:
                            SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=0,
                                                                                          status=0)
                else:
                    SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=1)

                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='root')
                ansible3.run(hosts=ips, module="shell",
                             args="free -m | grep 'Mem:' ")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    memall = re.findall("\d+",stdout_dict['success'][ips]['stdout'])
                    minfo = memall[1] + "/" + memall[0] + "Mb"
                    membl = int(float(int(memall[1]) * 100 / int(memall[0])))
                    if membl > 87:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                                      status=1)
                    elif membl > 70 and membl < 87:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                                      status=2)
                    else:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                              status=0)
                else:
                    SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=1)



            elif (ConnctUser.objects.filter(id=x.username).values('name').first())['name'] == 'root':
                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='root')
                ansible3.run(hosts=ips, module="shell",args="top -bn1 | grep load | awk '{printf $(NF-2)}'|awk -F ',' '{print $1}' ")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    cus = Host.objects.filter(resource_type=(ResourceType.objects.get(name='主机')).id,ostp='Linux',ipaddress=ips).values('cpus').exclude(ipaddress="").first()['cpus']
                    if cus is not None:
                        cpubl = (int(float(stdout_dict['success'][ips]['stdout']) * 100 / cus))
                        SystemHealthInfo.objects.create(ipaddress=ips,
                                                            cpublance=cpubl,
                                                            cpus=cus,
                                                            check_time=time.localtime())
                    else:
                        cpubl = 100
                        SystemHealthInfo.objects.create(ipaddress=ips,
                                                        cpublance=100,
                                                        cpus=cus,
                                                        check_time=time.localtime())

                    if cpubl > 85:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=2)
                    else:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=0)
                else:
                    SystemHealthInfo.objects.create(ipaddress=ips, status=1,check_time=time.localtime())

                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='root')
                ansible3.run(hosts=ips, module="shell",
                             args="df -h  | grep -vE '^Filesystem|tmpfs|cdrom|overlay|boot' | awk 'NR>1{print}'")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    dsinfo = stdout_dict['success'][ips]['stdout']
                    matchlist = re.findall("\d+%", dsinfo)
                    for x in matchlist:
                        if int(x.split("%")[0]) > 70 and int(x.split("%")[0]) < 85:
                            SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=2,
                                                                                          status=2)
                        elif int(x.split("%")[0]) > 85:
                            SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=1,
                                                                                          status=1)
                            break
                        else:
                            SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(diskinfo=dsinfo, diskstatus=0,
                                                                                          status=0)

                else:
                    SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=1)

                ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='root')
                ansible3.run(hosts=ips, module="shell",
                             args="free -m | grep 'Mem:'  ")
                stdout_dict = json.loads(ansible3.get_result())
                if stdout_dict['success'].get(ips):
                    memall = re.findall("\d+",stdout_dict['success'][ips]['stdout'])
                    minfo = memall[1] + "/" + memall[0] + "Mb"
                    membl = int(float(int(memall[1])*100/ int(memall[0])))
                    if membl > 87:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                                      status=1)
                    elif membl > 70 and membl < 87:
                        SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                                      status=2)
                    else:
                        SystemHealthInfo.objects.filter(ipaddress=ips, check_time=time.localtime()).update(meminfo=minfo, memblance=membl,
                                                                                      status=0)
                else:
                    SystemHealthInfo.objects.filter(ipaddress=ips,check_time=time.localtime()).update(status=1)

        except Exception as e:
            logger.error(msg="scan host hard health error->" + str(traceback.format_exc()))

        logger.info(msg="------ scan host health done -----------")
