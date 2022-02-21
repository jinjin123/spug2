import unittest
from apps.config.models import *
from apps.host.models import *
from libs.ansible29 import *
import re

class Mytest(unittest.TestCase):
     def test_get_disk(self):
         # hosts = Host.objects.filter(resource_type=(ResourceType.objects.get(name='主机')).id,
         #                             ostp='Linux').all().exclude(ipaddress="")
         # for x in hosts:
         #     print(x.ipaddress)
         ansible3 = MyAnsiable2(inventory='/etc/ansible/hosts', connection='smart', remote_user='jin')
         ansible3.run(hosts='127.0.0.1', module="shell",args="free -m | grep '内存'  ")
         stdout_dict = json.loads(ansible3.get_result())
         # print(stdout_dict)
         dsinfo = stdout_dict['success']['127.0.0.1']['stdout']
         memall = re.findall("\d+",dsinfo)
         minfo = memall[1] + "/" + memall[0] + "Mb"
         print(memall,minfo,int(float(int(memall[1])*100/ int(memall[0]))))
