# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
import datetime

from django.views.generic import View
from django.db.models import F
from libs import json_response, JsonParser, Argument,RequestApiAgent
from apps.app.models import Deploy,RancherConfigMap,RancherNamespace,RancherConfigMapVersion,RancherProject
from apps.config.models import *
import json
from django.conf import settings
import logging
logger = logging.getLogger('spug_log')

class RancherNsView(View):
    def get(self, request):
        # v2.3.14 临时数据初始化
        ns = list(RancherNamespace.objects.all().values("id","namespace"))
        return json_response(ns)

class RancherConfConfView(View):
    def get(self, request):
        # v2.3.14 临时数据初始化
        conf = list(RancherConfigMap.objects.all().values("id","configid","namespace_id","configMap_k","configMap_v"))
        # tmp = {}
        # tmp["conf"] = conf
        return json_response(conf)

class RancherAggMap(View):
    def get(self,request):
        conf = RancherConfigMap.objects.all()
        tmp = []
        for item in conf:
            data = item.to_dict(excludes=("create_by_id","namespace_id","modify_time"))
            tmp.append(data)
        return json_response(tmp)



class EnvironmentView(View):
    def get(self, request):
        query = {}
        if not request.user.is_supper:
            query['id__in'] = request.user.deploy_perms['envs']
        envs = Environment.objects.filter(**query)
        return json_response(envs)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('name', help='请输入环境名称'),
            Argument('key', help='请输入唯一标识符'),
            Argument('desc', required=False)
        ).parse(request.body)
        if error is None:
            form.key = form.key.replace("'", '')
            env = Environment.objects.filter(key=form.key).first()
            if env and env.id != form.id:
                return json_response(error=f'唯一标识符 {form.key} 已存在，请更改后重试')
            if form.id:
                Environment.objects.filter(pk=form.id).update(**form)
            else:
                env = Environment.objects.create(created_by=request.user, **form)
                if request.user.role:
                    request.user.role.add_deploy_perm('envs', env.id)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            if Config.objects.filter(env_id=form.id).exists():
                return json_response(error='该环境已存在关联的配置信息，请删除相关配置后再尝试删除')
            if Deploy.objects.filter(env_id=form.id).exists():
                return json_response(error='该环境已关联了发布配置，请删除相关发布配置后再尝试删除')
            Environment.objects.filter(pk=form.id).delete()
        return json_response(error=error)


class ServiceView(View):
    def get(self, request):
        services = Service.objects.all()
        return json_response(services)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('name', help='请输入服务名称'),
            Argument('key', help='请输入唯一标识符'),
            Argument('desc', required=False)
        ).parse(request.body)
        if error is None:
            service = Service.objects.filter(key=form.key).first()
            if service and service.id != form.id:
                return json_response(error=f'唯一标识符 {form.key} 已存在，请更改后重试')
            if form.id:
                Service.objects.filter(pk=form.id).update(**form)
            else:
                Service.objects.create(created_by=request.user, **form)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            if Config.objects.filter(type='src', o_id=form.id).exists():
                return json_response(error='该服务已存在关联的配置信息，请删除相关配置后再尝试删除')
            Service.objects.filter(pk=form.id).delete()
        return json_response(error=error)

class RancherConfManagerView(View):
    def get(self, request):
        form, error = JsonParser(
            Argument('configid',  help='configid丢失'),
            Argument('old_id', type=int, help='老配置id丢失'),
        ).parse(request.GET)
        config = RancherConfigMapVersion.objects.filter(old_id=form.old_id)
        tmp = []
        for item in config:
            cc = item.to_dict(excludes=("create_by_id","namespace_id","modify_time"))
            tmp.append(cc)
        return json_response(tmp)

    def post(self,request):
        form, error = JsonParser(
            # Argument('id', type=int, required=False),
            Argument('configMap_k',required=True, help='请输入映射key'),
            Argument('configMap_v',required=True,  help='请输入映射value'),
            Argument('configname',required=True,help='请输入配置文件名'),
            Argument('namespace',required=True, help="请输入命名空间"),
            Argument('project', required=True, help="请输入项目名"),
            # Argument('configid', required=False),
            # Argument('o_id', required=False),
            Argument('envs', type=list, filter=lambda x: len(x), help='请选择环境'),
        ).parse(request.body)
        if error is None:
            envs = form.pop('envs')
            cn = RancherConfigMap.objects.filter(configname=form.configname)
            if cn:
              return json_response(error='配置文件名已存在')
            global kwargs
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"},
                "data": {},
            }
            nstmp = form.pop("namespace")
            pj = RancherProject.objects.filter(project_name=form.pop("project")).first()
            ns = RancherNamespace.objects.filter(namespace=nstmp).first()
            try:
                tmp = {
                    "type": "configMap",
                    "data": {form.configMap_k: form.configMap_v},
                    "name": form.configname,
                    "namespaceId": nstmp
                }
                for env_id in envs:
                    if env_id == 1:
                        Action = RancherApiConfig.objects.filter(env_id=1,label="ADDCONFIGMAP").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(pj.project_id)
                        kwargs["data"] = json.dumps(tmp)
                        logger.info(msg="rancher configmap create args: " + str(kwargs))
                        res = json.loads(RequestApiAgent().create(**kwargs).content)
                        logger.info(msg="rancher configmap create call: " + json.dumps(res))
                        RancherConfigMap.objects.create(env_id=env_id, project=pj, namespace=ns, configid=res["id"],create_by=request.user, **form)
                    if env_id == 2:
                        Action = RancherApiConfig.objects.filter(env_id=2,label="ADDCONFIGMAP").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(pj.project_id)
                        kwargs["data"] = json.dumps(tmp)
                        logger.info(msg="rancher configmap create args: " + str(kwargs))
                        res = json.loads(RequestApiAgent().create(**kwargs).contnet)
                        logger.info(msg="rancher configmap create call: " + json.dumps(res))
                        RancherConfigMap.objects.create(env_id=env_id,project=pj, namespace=ns,configid=res["id"],create_by=request.user,**form)
            except Exception as e:
                logger.error(kwargs)
                logger.error("create rancher configmap err: "+ str(e))
                return json_response(error=str(e))
        return json_response(error=error)

    def put(self,request):
        form, error = JsonParser(
            Argument('project',  required=True),
            Argument('project_id',  required=True),
            Argument('configMap_k', help='请输入映射key'),
            Argument('configMap_v', help='请输入映射value'),
            Argument('configname', required=False),
            Argument('namespace', required=False),
            Argument('configid', required=True),
            Argument('old_id', required=False),
            Argument('envs', type=list, filter=lambda x: len(x), help='请选择环境'),
        ).parse(request.body)
        if error is None:
            config = RancherConfigMap.objects.filter(id=form.old_id)
            if not config:
                return json_response(error='未找到指定对象')
            project_id = form.pop("project_id")
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"},
                "data": json.dumps({"data":{form.configMap_k:form.configMap_v}})
            }

            RancherConfigMap.objects.filter(id=form.old_id).update(configMap_v=form.configMap_v,modify_time=datetime.datetime.now())
            envs = form.pop('envs')
            map_obj_v = list(config)[0].configMap_v
            new_v = form.pop("configMap_v")
            pj = RancherProject.objects.filter(project_name=form.pop("project")).first()
            try:
                for env_id in envs:
                    if env_id == 1:
                        Action = RancherApiConfig.objects.filter(env_id=1, label="PUTCONFIGMAP").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(project_id,form.configid)
                        res = RequestApiAgent().put(**kwargs).content
                        logger.info(msg="rancher update dev  configmap call: " + str(res))
                    if env_id == 2:
                        Action = RancherApiConfig.objects.filter(env_id=2, label="PUTCONFIGMAP").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(project_id,form.configid)
                        res = RequestApiAgent().put(**kwargs).content
                        logger.info(msg="rancher update prod  configmap call: " + str(res))

                    RancherConfigMapVersion.objects.create(env_id=env_id,project=pj,create_by=request.user,configMap_v=map_obj_v,**form)
            except Exception as  e:
                logger.error("rancher update configmap faild: " + str(e))

        return json_response(error=error)

class ConfigView(View):
    def get(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='未指定操作对象'),
            Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数'),
            Argument('env_id', type=int, help='缺少必要参数'),
        ).parse(request.GET)
        if error is None:
            form.o_id, data = form.pop('id'), []
            for item in Config.objects.filter(**form).annotate(update_user=F('updated_by__nickname')):
                tmp = item.to_dict()
                tmp['update_user'] = item.update_user
                data.append(tmp)
            return json_response(data)
        return json_response(error=error)

    def post(self, request):
        form, error = JsonParser(
            Argument('o_id', type=int, help='缺少必要参数'),
            Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数'),
            Argument('envs', type=list, filter=lambda x: len(x), help='请选择环境'),
            Argument('key', help='请输入Key'),
            Argument('is_public', type=bool, help='缺少必要参数'),
            Argument('value', type=str, default=''),
            Argument('desc', required=False)
        ).parse(request.body)
        if error is None:
            form.value = form.value.strip()
            form.updated_at = human_datetime()
            form.updated_by = request.user
            envs = form.pop('envs')
            for env_id in envs:
                Config.objects.create(env_id=env_id, **form)
                ConfigHistory.objects.create(action='1', env_id=env_id, **form)
        return json_response(error=error)

    def patch(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='缺少必要参数'),
            Argument('value', type=str, default=''),
            Argument('is_public', type=bool, help='缺少必要参数'),
            Argument('desc', required=False)
        ).parse(request.body)
        if error is None:
            form.value = form.value.strip()
            config = Config.objects.filter(pk=form.id).first()
            if not config:
                return json_response(error='未找到指定对象')
            config.desc = form.desc
            config.is_public = form.is_public
            if config.value != form.value:
                old_value = config.value
                config.value = form.value
                config.updated_at = human_datetime()
                config.updated_by = request.user
                ConfigHistory.objects.create(
                    action='2',
                    old_value=old_value,
                    **config.to_dict(excludes=('id',)))
            config.save()
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='未指定操作对象')
        ).parse(request.GET)
        if error is None:
            config = Config.objects.filter(pk=form.id).first()
            if config:
                ConfigHistory.objects.create(
                    action='3',
                    old_value=config.value,
                    value='',
                    updated_at=human_datetime(),
                    updated_by=request.user,
                    **config.to_dict(excludes=('id', 'value', 'updated_at', 'updated_by_id'))
                )
                config.delete()
        return json_response(error=error)


class HistoryView(View):
    def post(self, request):
        form, error = JsonParser(
            Argument('o_id', type=int, help='缺少必要参数'),
            Argument('env_id', type=int, help='缺少必要参数'),
            Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数')
        ).parse(request.body)
        if error is None:
            data = []
            for item in ConfigHistory.objects.filter(**form).annotate(update_user=F('updated_by__nickname')):
                tmp = item.to_dict()
                tmp['action_alias'] = item.get_action_display()
                tmp['update_user'] = item.update_user
                data.append(tmp)
            return json_response(data)
        return json_response(error=error)


def post_diff(request):
    form, error = JsonParser(
        Argument('o_id', type=int, help='缺少必要参数'),
        Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数'),
        Argument('envs', type=list, filter=lambda x: len(x), help='缺少必要参数'),
    ).parse(request.body)
    if error is None:
        data, form.env_id__in = {}, form.pop('envs')
        for item in Config.objects.filter(**form).order_by('key'):
            if item.key in data:
                data[item.key][item.env_id] = item.value
            else:
                data[item.key] = {'key': item.key, item.env_id: item.value}
        return json_response(list(data.values()))
    return json_response(error=error)


def parse_json(request):
    form, error = JsonParser(
        Argument('o_id', type=int, help='缺少必要参数'),
        Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数'),
        Argument('env_id', type=int, help='缺少必要参数'),
        Argument('data', type=dict, help='缺少必要参数')
    ).parse(request.body)
    if error is None:
        data = form.pop('data')
        _parse(request, form, data)
    return json_response(error=error)


def parse_text(request):
    form, error = JsonParser(
        Argument('o_id', type=int, help='缺少必要参数'),
        Argument('type', filter=lambda x: x in dict(Config.TYPES), help='缺少必要参数'),
        Argument('env_id', type=int, help='缺少必要参数'),
        Argument('data', handler=str.strip, help='缺少必要参数')
    ).parse(request.body)
    if error is None:
        data = {}
        for line in form.pop('data').split('\n'):
            line = line.strip()
            if not line or line[0] in ('#', ';'):
                continue
            fields = line.split('=', 1)
            if len(fields) != 2 or fields[0].strip() == '':
                return json_response(error=f'解析配置{line!r}失败，确认其遵循 key = value 格式')
            data[fields[0].strip()] = fields[1].strip()
        _parse(request, form, data)
    return json_response(error=error)


def _parse(request, query, data):
    for item in Config.objects.filter(**query):
        if item.key in data:
            value = _filter_value(data.pop(item.key))
            if item.value != value:
                old_value = item.value
                item.value = value
                item.updated_at = human_datetime()
                item.updated_by = request.user
                item.save()
                ConfigHistory.objects.create(
                    action='2',
                    old_value=old_value,
                    **item.to_dict(excludes=('id',)))
        else:
            ConfigHistory.objects.create(
                action='3',
                old_value=item.value,
                value='',
                updated_at=human_datetime(),
                updated_by=request.user,
                **item.to_dict(excludes=('id', 'value', 'updated_at', 'updated_by_id'))
            )
            item.delete()
    for key, value in data.items():
        query.key = key
        query.is_public = False
        query.value = _filter_value(value)
        query.updated_at = human_datetime()
        query.updated_by = request.user
        Config.objects.create(**query)
        ConfigHistory.objects.create(action='1', **query)


def _filter_value(value):
    if isinstance(value, (str, int)):
        value = str(value).strip()
    else:
        value = json.dumps(value)
    return value
