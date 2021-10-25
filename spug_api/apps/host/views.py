# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.views.generic import View
from django.db.models import F
from django.http.response import HttpResponseBadRequest
from libs import json_response, JsonParser, Argument
from apps.setting.utils import AppSetting
from apps.host.models import Host
from apps.app.models import Deploy
from apps.schedule.models import Task
from apps.monitor.models import Detection
from apps.account.models import Role
from libs.ssh import SSH, AuthenticationException
from paramiko.ssh_exception import BadAuthenticationType
from libs import human_datetime, AttrDict
from openpyxl import load_workbook
import socket
from apps.host.tasks import  *

class HostView(View):
    def get(self, request):
        host_id = request.GET.get('id')
        if host_id:
            if not request.user.has_host_perm(host_id):
                return json_response(error='无权访问该主机，请联系管理员')
            return json_response(Host.objects.get(pk=host_id))
        # hosts = Host.objects.filter(deleted_by_id__isnull=True)
        hosts = Host.objects.all()
        zones = [x['zone'] for x in hosts.order_by('zone').values('zone').distinct()]
        tp = [x['top_project'] for x in hosts.order_by('top_project').values('top_project').distinct()]
        ostp = [x["ostp"] for x in hosts.order_by('ostp').values('ostp').distinct() ]
        res_t = [x['resource_type'] for x in hosts.order_by('resource_type').values('resource_type').distinct()]
        w_z = [x['work_zone'] for x in hosts.order_by('work_zone').values('work_zone').distinct()]
        provider = [x['provider'] for x in hosts.order_by('provider').values('provider').distinct()]
        perms = [x.id for x in hosts] if request.user.is_supper else request.user.host_perms
        return json_response({"tp":tp,"ostp":ostp,'provider':provider,'w_z':w_z,'res_t':res_t,'zones': zones, 'hosts': [x.to_dict() for x in hosts], 'perms': perms})

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('zone', help='请输入分组类型'),
            # Argument('name', help='请输主机名称'),
            Argument('username', handler=str.strip, help='请输入登录用户名'),
            Argument('ipaddress', handler=str.strip, help='请输入主机名或IP'),
            Argument('port', type=int, help='请输入SSH端口'),
            Argument('pkey', required=False),
            # Argument('status', handler=str.strip,required=True,help='上线/下线status状态'),
            Argument('comment', required=False),
            Argument('password',handler=str.strip,  required=False),
            Argument('password_expire',type=int, required=False),

            Argument('ostp',type=str, required=False),
            Argument('resource_type',type=str, required=False),
            Argument('v_ip', required=False),
            Argument('outter_ip', required=False),
            Argument('provider', required=False),
            Argument('top_project', type=str,required=False),
            Argument('service_pack', required=False),
            Argument('work_zone', required=False),
            Argument('use_for', required=False),
            Argument('developer', required=False),
            Argument('opsper', required=False),
            Argument('env_id', required=False),
            Argument('ext_config1', required=False),

            # Argument('cpus',type=int, required=False),
            # Argument('memory', type=int, required=False),

        ).parse(request.body)
        if error is None:
            if form.top_project == "东莞市政务数据大脑暨智慧城市IOC运行中心建设项目":
                form.update({"top_projectid" : "dgdataheadioc"})
            elif form.top_project == "东莞市疫情动态查询系统项目":
                form.update({"top_projectid" : "dgdycovidselect"})
            elif form.top_project == "东莞市疫情防控数据管理平台项目":
                form.update({"top_projectid" : "dgcoviddatamanager"})
            elif form.top_project == "东莞市跨境货车司机信息管理系统项目":
                form.update({"top_projectid" : "dgdriverinfo"})
            elif form.top_project == "疫情地图项目":
                form.update({"top_projectid": "dgcovidmap"})
            elif form.top_project == "粤康码":
                form.update({"top_projectid" : "dghealthqr"})
            ppwd = form.pop('password')
            if form.ostp != "Windows" and form.resource_type == "主机" :
               if valid_ssh(form.ipaddress, form.port, form.username, password=ppwd,
                         pkey=form.pkey) is False:
                return json_response('auth fail')
            # form.pop("created_by")
            if form.id:
                pwd = Host.make_password(ppwd)
                Host.objects.filter(pk=form.pop('id')).update(**form,password_hash=pwd)
                return json_response(error=error)
            if Host.objects.filter(ipaddress=form.ipaddress).exists():
                return json_response(error=f'已存在的ip【{form.ipaddress}】')
            else:
                if form.ostp != "Windows" and form.resource_type == "主机" :
                    pwd = Host.make_password(ppwd)
                    host = Host.objects.create(create_by=request.user,  password_hash=pwd,**form)
                    update_hostinfo.delay([form.ipaddress], form.username)
                else:
                    pwd = Host.make_password(ppwd)
                    host = Host.objects.create(create_by=request.user, password_hash=pwd, **form)
                if request.user.role:
                    request.user.role.add_host_perm(host.id)
        return json_response(error=error)

    def patch(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('zone', help='请输入主机类别')
        ).parse(request.body)
        if error is None:
            host = Host.objects.filter(pk=form.id).first()
            if not host:
                return json_response(error='未找到指定主机')
            count = Host.objects.filter(zone=host.zone, deleted_by_id__isnull=True).update(zone=form.zone)
            return json_response(count)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            deploy = Deploy.objects.filter(host_ids__regex=fr'[^0-9]{form.id}[^0-9]').annotate(
                app_name=F('app__name'),
                env_name=F('env__name')
            ).first()
            if deploy:
                return json_response(error=f'应用【{deploy.app_name}】在【{deploy.env_name}】的发布配置关联了该主机，请解除关联后再尝试删除该主机')
            task = Task.objects.filter(targets__regex=fr'[^0-9]{form.id}[^0-9]').first()
            if task:
                return json_response(error=f'任务计划中的任务【{task.name}】关联了该主机，请解除关联后再尝试删除该主机')
            detection = Detection.objects.filter(type__in=('3', '4'), addr=form.id).first()
            if detection:
                return json_response(error=f'监控中心的任务【{detection.name}】关联了该主机，请解除关联后再尝试删除该主机')
            role = Role.objects.filter(host_perms__regex=fr'[^0-9]{form.id}[^0-9]').first()
            if role:
                return json_response(error=f'角色【{role.name}】的主机权限关联了该主机，请解除关联后再尝试删除该主机')
            trelease = Host.objects.filter(pk=form.id,zone="待回收").exists()
            if trelease:
                return json_response(error=f'主机已待回收')
            t = Host.objects.filter(pk=form.id).first()
            Host.objects.filter(pk=form.id).update(
                zone="待回收",
                ipaddress="",
                iprelease=t.ipaddress,
                deleted_at=human_datetime(),
                deleted_by=request.user,
            )
        return json_response(error=error)


def post_import(request):
    password = request.POST.get('password')
    file = request.FILES['file']
    ws = load_workbook(file, read_only=True)['Sheet1']
    summary = {'invalid': [], 'skip': [], 'fail': [], 'network': [], 'repeat': [], 'success': [], 'error': []}
    ioctmp = []
    roottmp = []
    for i, row in enumerate(ws.rows):
        if i == 0:  # 第1行是表头 略过
            continue
        # if not all([row[x].value for x in range(5)]):
        #     summary['invalid'].append(i)
        #     continue
        data = AttrDict(
            top_project=row[0].value,
            v_ip=row[1].value,
            outter_ip=row[2].value,
            ipaddress=row[3].value,
            username=row[4].value,
            port=row[5].value,
            password=row[6].value,
            password_expire=row[7].value,
            zone=row[8].value,
            ostp=row[9].value,
            provider=row[10].value,
            resource_type=row[11].value,
            work_zone=row[12].value,
            use_for=row[13].value,
            developer=row[14].value,
            opsper=row[15].value,
            service_pack=row[16].value,
            host_bug=row[17].value,
            ext_config1=row[18].value,
            env_id=row[19].value,
            comment=row[20].value
        )
        if Host.objects.filter(ipaddress=data.ipaddress, port=data.port, username=data.username).exists():
            # Host.objects.filter(ipaddress=data.ipaddress, port=data.port, username=data.username).update(create_by=request.user,**data)
            summary['skip'].append(i)
            continue
        try:
            if  data.ostp == "" or data.resource_type == "" or data.top_project == "" or data.ipaddress == "" or data.zone == "" \
                    or data.provider == "":
                summary['fail'].append(i)
                continue
            pwd = data.password
            if data.ostp == 'Linux' and data.resource_type =='主机' and valid_ssh(data.ipaddress, data.port, data.username, data.pop('password') or password, None,
                         False) is False:
                summary['fail'].append(i)
                continue
        except AuthenticationException:
            summary['fail'].append(i)
            continue
        except socket.error:
            summary['network'].append(i)
            continue
        except Exception:
            summary['error'].append(i)
            continue
        # if Host.objects.filter(name=data.name, deleted_by_id__isnull=True).exists():
        #     summary['repeat'].append(i)
        #     continue

        # if data.ostp == 'Windows':
        #     pwd = data.pop("password")
        data["password_hash"] = Host.make_password(pwd)
        data["env_id"] =  2 if data.env_id == "生产" else 1
        if data.top_project == "东莞市政务数据大脑暨智慧城市IOC运行中心建设项目":
            data.update({"top_projectid": "dgdataheadioc"})
        elif data.top_project == "东莞市疫情动态查询系统项目":
            data.update({"top_projectid": "dgdycovidselect"})
        elif data.top_project == "东莞市疫情防控数据管理平台项目":
            data.update({"top_projectid": "dgcoviddatamanager"})
        elif data.top_project == "东莞市跨境货车司机信息管理系统项目":
            data.update({"top_projectid": "dgdriverinfo"})
        elif data.top_project == "疫情地图项目":
            data.update({"top_projectid": "dgcovidmap"})
        elif data.top_project == "粤康码":
            data.update({"top_projectid": "dghealthqr"})
        host = Host.objects.create(create_by=request.user, **data)
        if data.username == "root":
            roottmp.append(data.ipaddress)
        elif data.username == "ioc":
            ioctmp.append(data.ipaddress)
        # tmp.append(data.ipaddress)
        # update_hostinfo.delay(tmp, 'root')
        if request.user.role:
            request.user.role.add_host_perm(host.id)
        summary['success'].append(i)
    update_hostinfo.delay(roottmp, 'root')
    update_hostinfo.delay(ioctmp, 'ioc')
    return json_response(summary)


def valid_ssh(hostname, port, username, password=None, pkey=None, with_expect=True):
    try:
        private_key = AppSetting.get('private_key')
        public_key = AppSetting.get('public_key')
    except KeyError:
        private_key, public_key = SSH.generate_key()
        AppSetting.set('private_key', private_key, 'ssh private key')
        AppSetting.set('public_key', public_key, 'ssh public key')
    if password:
        _cli = SSH(hostname, port, username, password=str(password))
        _cli.add_public_key(public_key)
    if pkey:
        private_key = pkey
    try:
        cli = SSH(hostname, port, username, private_key)
        cli.ping()
    except BadAuthenticationType:
        if with_expect:
            raise TypeError('该主机不支持密钥认证，请参考官方文档，错误代码：E01')
        return False
    except AuthenticationException:
        if password and with_expect:
            raise ValueError('密钥认证失败，请参考官方文档，错误代码：E02')
        return False
    return True


def post_parse(request):
    file = request.FILES['file']
    if file:
        data = file.read()
        return json_response(data.decode())
    else:
        return HttpResponseBadRequest()
