# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.views.generic import View
from django.db.models import F
from django.conf import settings
from libs import JsonParser, Argument, json_response,pvcargs,cmapargs,svcargs
from apps.app.models import *
from apps.config.models import Config, RancherApiConfig
from apps.app.utils import parse_envs, fetch_versions, remove_repo
from apps.account.models import User
from apps.message.models import LoggerOpRecord
import subprocess
import json
import os
from libs.utils import RequestApiAgent
import logging
from datetime import datetime
logger = logging.getLogger('spug_log')


class AppView(View):
    def get(self, request):
        # v2.3.14 临时数据初始化
        app = App.objects.first()
        if app and hasattr(app, 'sort_id') and app.sort_id == 0:
            for app in App.objects.all():
                app.sort_id = app.id
                app.save()
        query = {}
        if not request.user.is_supper:
            query['id__in'] = request.user.deploy_perms['apps']
        apps = App.objects.filter(**query)
        return json_response(apps)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('name', help='请输入服务名称'),
            Argument('key', help='请输入唯一标识符'),
            Argument('desc', required=False)
        ).parse(request.body)
        if error is None:
            form.name = form.name.replace("'", '')
            app = App.objects.filter(key=form.key).first()
            if app and app.id != form.id:
                return json_response(error=f'唯一标识符 {form.key} 已存在，请更改后重试')
            if form.id:
                App.objects.filter(pk=form.id).update(**form)
            else:
                app = App.objects.create(created_by=request.user, **form)
                app.sort_id = app.id
                app.save()
                if request.user.role:
                    request.user.role.add_deploy_perm('apps', app.id)
        return json_response(error=error)

    def patch(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='参数错误'),
            Argument('rel_apps', type=list, required=False),
            Argument('rel_services', type=list, required=False),
            Argument('sort', filter=lambda x: x in ('up', 'down'), required=False)
        ).parse(request.body)
        if error is None:
            app = App.objects.filter(pk=form.id).first()
            if not app:
                return json_response(error='未找到指定应用')
            if form.rel_apps is not None:
                app.rel_apps = json.dumps(form.rel_apps)
            if form.rel_services is not None:
                app.rel_services = json.dumps(form.rel_services)
            if form.sort:
                if form.sort == 'up':
                    tmp = App.objects.filter(sort_id__gt=app.sort_id).last()
                else:
                    tmp = App.objects.filter(sort_id__lt=app.sort_id).first()
                if tmp:
                    tmp.sort_id, app.sort_id = app.sort_id, tmp.sort_id
                    tmp.save()
            app.save()
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            if Deploy.objects.filter(app_id=form.id).exists():
                return json_response(error='该应用在应用发布中已存在关联的发布配置，请删除相关发布配置后再尝试删除')
            if Config.objects.filter(type='app', o_id=form.id).exists():
                return json_response(error='该应用在配置中心已存在关联的配置信息，请删除相关配置后再尝试删除')
            App.objects.filter(pk=form.id).delete()
        return json_response(error=error)


class DeployView(View):
    def get(self, request):
        form, error = JsonParser(
            Argument('app_id', type=int, required=False)
        ).parse(request.GET, True)
        if not request.user.is_supper:
            perms = request.user.deploy_perms
            form.app_id__in = perms['apps']
            form.env_id__in = perms['envs']
        deploys = Deploy.objects.filter(**form).annotate(app_name=F('app__name')).order_by('-app__sort_id')
        return json_response(deploys)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('app_id', type=int, help='请选择应用'),
            Argument('env_id', type=int, help='请选择环境'),
            Argument('host_ids', type=list, filter=lambda x: len(x), help='请选择要部署的主机'),
            Argument('rst_notify', type=dict, help='请选择发布结果通知方式'),
            Argument('extend', filter=lambda x: x in dict(Deploy.EXTENDS), help='请选择发布类型'),
            Argument('is_audit', type=bool, default=False)
        ).parse(request.body)
        if error is None:
            deploy = Deploy.objects.filter(app_id=form.app_id, env_id=form.env_id).first()
            if deploy and deploy.id != form.id:
                return json_response(error='应用在该环境下已经存在发布配置')
            form.host_ids = json.dumps(form.host_ids)
            form.rst_notify = json.dumps(form.rst_notify)
            if form.extend == '1':
                extend_form, error = JsonParser(
                    Argument('git_repo', handler=str.strip, help='请输入git仓库地址'),
                    Argument('dst_dir', handler=str.strip, help='请输入发布目标路径'),
                    Argument('dst_repo', handler=str.strip, help='请输入目标仓库路径'),
                    Argument('versions', type=int, help='请输入保留历史版本数量'),
                    Argument('filter_rule', type=dict, help='参数错误'),
                    Argument('custom_envs', handler=str.strip, required=False),
                    Argument('hook_pre_server', handler=str.strip, default=''),
                    Argument('hook_post_server', handler=str.strip, default=''),
                    Argument('hook_pre_host', handler=str.strip, default=''),
                    Argument('hook_post_host', handler=str.strip, default='')
                ).parse(request.body)
                if error:
                    return json_response(error=error)
                extend_form.dst_dir = extend_form.dst_dir.rstrip('/')
                extend_form.filter_rule = json.dumps(extend_form.filter_rule)
                extend_form.custom_envs = json.dumps(parse_envs(extend_form.custom_envs))
                if form.id:
                    extend = DeployExtend1.objects.filter(deploy_id=form.id).first()
                    if extend.git_repo != extend_form.git_repo:
                        remove_repo(form.id)
                    Deploy.objects.filter(pk=form.id).update(**form)
                    DeployExtend1.objects.filter(deploy_id=form.id).update(**extend_form)
                else:
                    deploy = Deploy.objects.create(created_by=request.user, **form)
                    DeployExtend1.objects.create(deploy=deploy, **extend_form)
            elif form.extend == '2':
                extend_form, error = JsonParser(
                    Argument('server_actions', type=list, help='请输入执行动作'),
                    Argument('host_actions', type=list, help='请输入执行动作')
                ).parse(request.body)
                if error:
                    return json_response(error=error)
                if len(extend_form.server_actions) + len(extend_form.host_actions) == 0:
                    return json_response(error='请至少设置一个执行的动作')
                extend_form.server_actions = json.dumps(extend_form.server_actions)
                extend_form.host_actions = json.dumps(extend_form.host_actions)
                if form.id:
                    Deploy.objects.filter(pk=form.id).update(**form)
                    DeployExtend2.objects.filter(deploy_id=form.id).update(**extend_form)
                else:
                    deploy = Deploy.objects.create(created_by=request.user, **form)
                    DeployExtend2.objects.create(deploy=deploy, **extend_form)
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            Deploy.objects.filter(pk=form.id).delete()
            repo_dir = os.path.join(settings.REPOS_DIR, str(form.id))
            subprocess.Popen(f'rm -rf {repo_dir} {repo_dir + "_*"}', shell=True)
        return json_response(error=error)

class RancherSvcNoticeView(View):
    def get(self,request):
        ob = ProjectServiceApprovalNotice.objects.all()
        pj = [x['service__top_project'] for x in ob.values('service__top_project').distinct()]
        rj = [x['service__pjname'] for x in ob.values('service__pjname').distinct()]
        return json_response({"pj":pj,"rj":rj,"data": [x.to_dict() for x in ob]})

    def post(self,request):
        form, error = JsonParser(
            Argument('tj', help='请输入实体项目'),
            Argument('rj', help='请输入rancher项目'),
            Argument('us', help= '请输入用户名'),
            Argument('ns', help='请输入命名空间'),
            Argument('app',  help='请输入应用'),
        ).parse(request.body)
        if error is None:
            pj = ProjectService.objects.filter(top_project=form.tj,pjname=form.rj,nsname=form.ns,dpname=form.app).first()
            if pj is None:
                return json_response(error=f'应用对应不上项目，请重新查询绑定')
            us = User.objects.filter(nickname=form.us).first()

            m = ProjectServiceApprovalNotice.objects.create(service=pj,notice_user=us)
            m.save()
        return json_response(error=error)

    def delete(self,request):
        form, error = JsonParser(
            Argument('id', type=int, help='请指定操作对象')
        ).parse(request.GET)
        if error is None:
            ProjectServiceApprovalNotice.objects.filter(pk=form.id).delete()
        return json_response(error=error)


class RancherSvcView(View):
    def get(self,request,tag):
        # svc = RancherDeployment.objects.all()
        svc = ""
        cmap= ""
        pvc=""
        nodes=""
        if tag == "ioc":
            svc = ProjectService.objects.filter(rancher_url__contains="ioc").all()
            cmap = ProjectConfigMap.objects.filter(tag='ioc').all()
            pvc  = ProjectPvc.objects.filter(tag='ioc').all()
            nodes = RancherNode.objects.filter(tag='ioc').all()
        elif tag == "fangyi":
            svc = ProjectService.objects.filter(rancher_url__contains="feiyan.com").all()
            cmap = ProjectConfigMap.objects.filter(tag='feiyan').all()
            pvc = ProjectPvc.objects.filter(tag='feiyan').all()
            nodes = RancherNode.objects.filter(tag='feiyan').all()
        elif tag == "fangyiuos":
            svc = ProjectService.objects.filter(rancher_url__contains="feiyan.uos").all()
            cmap = ProjectConfigMap.objects.filter(tag='feiyanuos').all()
            pvc = ProjectPvc.objects.filter(tag='feiyanuos').all()
            nodes = RancherNode.objects.filter(tag='feiyanuos').all()
        else:
            svc = ProjectService.objects.all()
            cmap = ProjectConfigMap.objects.all()
            pvc = ProjectPvc.objects.all()
            nodes = RancherNode.objects.all()
        pj = [x['top_project'] for x in svc.order_by('top_project').values('top_project').distinct()]
        rj = [x['pjname'] for x in svc.order_by('pjname').values('pjname').distinct()]
        ns = [x['nsname'] for x in svc.order_by('nsname').values('nsname').distinct()]
        app = [x['dpname'] for x in svc.order_by('dpname').values('dpname').distinct()]
        # tmp = []
        # for item in svc:
            # data = item.to_dict(excludes=("create_by_id", "project_id", "namespace_id", "modify_time"))
            # data = item.to_dict()
            # tmp.append(data)
        return json_response({"pj":pj,"rj":rj,"ns": ns,"app":app,'cmap':[x.to_dict() for x in cmap],
                              "pvc": [x.to_dict() for x in pvc],
                              "svc":[x.to_dict() for x in svc],"nodes":[x.to_dict() for x in nodes]})

    def post(self,request):
        form, error = JsonParser(
            Argument('project_id', required=True, help='项目id'),
            Argument('deployid', required=True, help='应用id'),
            Argument('env_id',type=int,required=True, help='环境id'),
        ).parse(request.body)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            try:
                logger.info(msg="#######redeploy pod start ########")
                if form.env_id == 1:
                    Action = RancherApiConfig.objects.filter(env_id=1, label="REDOSVC").first()
                    kwargs["headers"]["Authorization"] = Action.token
                    kwargs["url"] = (Action.url).format(form.project_id,form.deployid)
                    res = RequestApiAgent().create(**kwargs)
                    logger.info(msg="#####rancher redploy dev call:###### " + str(res.status_code))
                    if res.status_code != 200:
                        logger.error(msg="#####rancher redploy dev call:###### " + str(res))
                        return json_response(error="重新部署rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                if form.env_id == 2:
                    #todo change api
                    Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC").first()
                    kwargs["headers"]["Authorization"] = Action.token
                    kwargs["url"] = (Action.url).format(form.project_id,form.deployid)
                    res = RequestApiAgent().create(**kwargs)
                    logger.info(msg="#####rancher redploy prod call:###### " + str(res.status_code))
                    if res.status_code != 200:
                        logger.error(msg="#####rancher redploy prod call:###### " + str(res))
                        return json_response(error="重新部署rancher api 出现异常，请重试一次！如还有问题请联系运维！")
            except Exception as  e:
                logger.error("#######redeploy pod faild: ########"+ str(e))
                return json_response(error=str(e))

        return json_response(error=error)



    def put(self,request):
        pass

    def delete(self,request):
        pass


# class DeployRancherNsView(View):
#     def get(self, request):
#         # v2.3.14 临时数据初始化
#         ns = list(RancherNamespace.objects.all().values("id","namespace"))
#         # conf = list(RancherConfigMap.objects.all().values("configid"))
#         # tmp = {}
#         # tmp["ns"] = ns
#         # tmp["conf"] = conf
#         # if not request.user.is_supper:
#         #     query['id__in'] = request.user.deploy_perms['apps']
#         return json_response(ns)
#
# class DeployRancherConfView(View):
#     def get(self, request):
#         # v2.3.14 临时数据初始化
#         conf = list(RancherConfigMap.objects.all().values("id","configid","namespace_id","configMap_k","configMap_v"))
#         # tmp = {}
#         # tmp["conf"] = conf
#         return json_response(conf)



def get_versions(request, d_id):
    deploy = Deploy.objects.filter(pk=d_id).first()
    if not deploy:
        return json_response(error='未找到指定应用')
    if deploy.extend == '2':
        return json_response(error='该应用不支持此操作')
    branches, tags = fetch_versions(deploy)
    return json_response({'branches': branches, 'tags': tags})

class RancherPvcOpView(View):
    def post(self,request):
        form, error = JsonParser(
            Argument('data', required=False,type=dict, help='pvcdata'),
            Argument('env', required=False, type=int, help='env'),
            Argument('tag', required=False, type=str, help='tag'),
        ).parse(request.body)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            tmptag = ""
            if form.tag == "feiyanuos":
                 tmptag = "feiyan.uos"
            elif form.tag == "feiyan":
                tmptag = "feiyan.com"
            elif form.tag == "ioc":
                tmptag = "ioc.com"
            ex = ProjectService.objects.filter(pjname=(form.data)['pjname'],verifyurl__contains=tmptag).values('pjid')
            if ex.exists():
                d = ex.first()
                global pvarg
                Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETPVC",tag=form.tag ).first()
                kwargs["headers"]["Authorization"] = Action.token
                kwargs["url"] = (Action.url).format(d['pjid'])
                if (form.data).get("storageClassId"):
                    pvarg = pvcargs(1)
                    pvarg["storageClassId"] = (form.data)['storageClassId']
                    pvarg["name"] = (form.data)['name']
                    pvarg["resources"]["requests"]["storage"] = (form.data)["resources"]["requests"]["storage"]
                    pvarg['namespaceId'] = (form.data)['namespaceId']
                else:
                    pvarg = pvcargs(0)
                    pvarg["name"] = (form.data)['name']
                    pvarg["resources"]["requests"]["storage"] = (form.data)["resources"]["requests"]["storage"]
                    pvarg['namespaceId'] = (form.data)['namespaceId']
                kwargs['data'] = json.dumps(pvarg)
                res = RequestApiAgent().create(**kwargs)
                logger.info(msg="#####rancher redploy pvc call:###### " + str(res.status_code))
                red = json.loads(res.content)
                if res.status_code != 201:
                    logger.error(msg="#####rancher redploy dev call:###### " + str(res))
                    return json_response(error="重新部署rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                vfurl = ""
                if form.tag == "ioc":
                    vfurl = "https://rancher.ioc.com/p/"+red['projectId']+'/volumes/'+ red['id']
                elif form.tag == "feiyan":
                    vfurl = "https://rancher.feiyan.com/p/"+red['projectId']+'/volumes/'+ red['id']
                elif form.tag == "feiyanuos":
                    vfurl = "https://rancher.feiyan.uos.com/p/"+red['projectId']+'/volumes/'+ red['id']
                m = ProjectPvc.objects.create(
                    pjid=red['projectId'],
                    nsname=red['namespaceId'],
                    nsid=red['namespaceId'],
                    pvcid=red['id'],
                    pvcname=red['name'],
                    storageid=red['storageClassId'],
                    capacity=red['resources']['requests']['storage'],
                    accessMode=red['accessModes'],
                    volumeid='pvc-'+ red['uuid'],
                    dellinks=red["links"]["remove"],
                    selflinks=red["links"]["self"],
                    updatelinks=red["links"]["update"],
                    yamllinks=red["links"]["yaml"],
                    tag=form.tag,
                    verifyurl=vfurl,
                    create_by=request.user,
                    pjname=(ProjectService.objects.filter(pjid=red['projectId']).first()).pjname
                )
                m.save()
                LoggerOpRecord.objects.create(create_by=request.user, content="Createpvc:" + red['name']+str(request.user.nickname),
                                          action="create")

        return json_response(error=error)

    def delete(self,request):
        form, error = JsonParser(
            Argument('id', type=int, help='id'),
            Argument('env',type=int, help='env'),
            Argument('tag', type=str, help='tag'),
        ).parse(request.GET)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            m = ProjectPvc.objects.filter(id=form.id).first()
            Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETPVC",tag=form.tag).first()
            kwargs["headers"]["Authorization"] = Action.token
            kwargs["url"] = m.dellinks
            res = RequestApiAgent().delete(**kwargs)
            if res.status_code != 200:
                logger.error(msg="#####rancher remove pvc call:###### " + str(res))
                return json_response(error="删除rancher pvc api 出现异常，请重试一次！如还有问题请联系运维！")
            ProjectPvc.objects.filter(id=form.id).delete()

        return json_response(error=error)

class RancherCmapOpView(View):
    def post(self,request):
        form, error = JsonParser(
            Argument('data', required=False,type=dict, help='cmapdata'),
            Argument('env', required=False, type=int, help='env'),
            Argument('tag', required=False, type=str, help='tag'),
        ).parse(request.body)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            tmptag = ""
            if form.tag == "feiyanuos":
                 tmptag = "feiyan.uos"
            elif form.tag == "feiyan":
                tmptag = "feiyan.com"
            elif form.tag == "ioc":
                tmptag = "ioc.com"

            if (form.data)['newNs']:
                global Action
                if (form.data)['pjname'] == "自动化发布":
                    Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETSIGNS", tag=form.tag).first()
                else:
                    Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETNS", tag=form.tag).first()
                kwargs["headers"]["Authorization"] = Action.token
                kwargs["url"] = Action.url
                kwargs['data'] = json.dumps({"type":"namespace","name":(form.data)['namespaceId'],"projectId": (ProjectService.objects.filter(pjname=(form.data)['pjname']).first()).pjid})
                logger.info(msg="#####rancher create namespace######")
                res = RequestApiAgent().create(**kwargs)
                if res.status_code != 201:
                    logger.error(msg="#####rancher create namespace error###### --->" + str(res.status_code) + str(res.content))
                    return json_response(error="创建新命名空间失败 请重试一次！如还有问题请联系运维！")
                LoggerOpRecord.objects.create(create_by=request.user,content="CreateNs:" + str(request.user.nickname),action="create")

            cmap = cmapargs()
            cmap['data'] = (form.data)['data']
            cmap['name']=  (form.data)['name']
            cmap['namespaceId']= (form.data)['namespaceId']
            Action = RancherApiConfig.objects.filter(env_id=form.env, label="ADDCONFIGMAP",tag=form.tag).first()
            kwargs["headers"]["Authorization"] = Action.token
            kwargs["url"] = (Action.url).format((ProjectConfigMap.objects.filter(pjname=(form.data)['pjname'],verifyurl__contains=tmptag).first()).pjid)
            kwargs['data'] = json.dumps(cmap)
            res = RequestApiAgent().create(**kwargs)
            logger.info(msg="#####rancher create cmap call:###### " + str(res.status_code))
            red = json.loads(res.content)
            if res.status_code != 201:
                logger.error(msg="#####rancher create configmap call:###### " + str(red))
                return json_response(error="重新部署rancher configmap api 出现异常，请重试一次！如还有问题请联系运维！")
            vfurl = ""
            if form.tag == "ioc" :
                vfurl = "https://rancher.ioc.com/p/"+red['projectId']+'/config-maps/'+ red['id']
            elif form.tag == "feiyan":
                vfurl = "https://rancher.feiyan.com/p/"+red['projectId']+'/config-maps/'+ red['id']
            elif form.tag == "feiyanuos":
                vfurl = "https://rancher.feiyan.uos.com/p/" + red['projectId'] + '/config-maps/' + red['id']
            m = ProjectConfigMap.objects.create(
                pjid=red['projectId'],
                configId=red['id'],
                configName=red['name'],
                configMap=(form.data)['dbdata'],
                nsname=red['namespaceId'],
                nsid=red['namespaceId'],
                dellinks=red["links"]["remove"],
                selflinks=red["links"]["self"],
                updatelinks=red["links"]["update"],
                yamllinks=red["links"]["yaml"],
                tag=form.tag,
                create_by=request.user,
                verifyurl=vfurl,
                pjname=(ProjectService.objects.filter(pjid=red['projectId']).first()).pjname,
            )
            m.save()
            LoggerOpRecord.objects.create(create_by=request.user,content="Createcmap:" + red['name'] + str(request.user.nickname),
                                          action="create")
        return json_response(error=error)


    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='id'),
            Argument('env', type=int, help='env'),
            Argument('tag', required=False, type=str, help='tag'),
        ).parse(request.GET)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            m = ProjectConfigMap.objects.filter(id=form.id).first()
            Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETPVC",tag=form.tag).first()
            kwargs["headers"]["Authorization"] = Action.token
            kwargs["url"] = m.dellinks
            res = RequestApiAgent().delete(**kwargs)
            if res.status_code != 204:
                logger.error(msg="#####rancher remove cmap call:###### " + str(res))
                return json_response(error="删除rancher configmap api 出现异常，请重试一次！如还有问题请联系运维！")
            ProjectConfigMap.objects.filter(id=form.id).delete()

        return json_response(error=error)

class RancherSvcOpView(View):
    def post(self,request):
        form, error = JsonParser(
            Argument('data', required=False,type=dict, help='cmapdata'),
            Argument('env', required=False, type=int, help='env'),
            Argument('tag', required=False, type=str, help='tag'),
        ).parse(request.body)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }
            if (form.data)['newNs']:
                global Action
                if (form.data)['pjname'] == "自动化发布":
                    Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETSIGNS", tag=form.tag).first()
                else:
                    Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETNS", tag=form.tag).first()
                kwargs["headers"]["Authorization"] = Action.token
                kwargs["url"] = Action.url
                kwargs['data'] = json.dumps({"type":"namespace","name":(form.data)['namespaceId'],"projectId": (ProjectService.objects.filter(pjname=(form.data)['pjname']).first()).pjid})
                logger.info(msg="#####rancher create namespace######")
                res = RequestApiAgent().create(**kwargs)
                if res.status_code != 201:
                    logger.error(msg="#####rancher create namespace error###### --->" + str(res.status_code) + str(res.content))
                    return json_response(error="创建新命名空间失败 请重试一次！如还有问题请联系运维！")
                LoggerOpRecord.objects.create(create_by=request.user,content="CreateNs:" + str(request.user.nickname),action="create")

            svc = svcargs()
            svc['scheduling'] = (form.data)['scheduling']
            svc['volumes'] = (form.data)['volumes']
            svc['name'] = (form.data)['name']
            svc['scale'] = (form.data)['scale']
            svc['namespaceId'] = (form.data)['namespaceId']
            svc['containers'][0]['ports'] =  (form.data)['ports']
            svc['containers'][0]['namespaceId'] =  (form.data)['namespaceId']
            svc['containers'][0]['image'] =  (form.data)['image']
            svc['containers'][0]['name'] =  (form.data)['name']
            svc['containers'][0]['environment'] =  (form.data)['environment']
            svc['containers'][0]['volumeMounts'] =  (form.data)['volumeMounts']

            logger.info(msg="#####rancher create deployment start:###### ")

            Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETSVC", tag=form.tag).first()
            global newUrl
            newUrl = ""
            if form.tag == "feiyanuos":
                newUrl = (Action.url).format((ProjectService.objects.filter(pjname=(form.data)['pjname'],rancher_url__contains="feiyan.uos").first()).pjid)
            elif form.tag == "feiyan":
                newUrl = (Action.url).format((ProjectService.objects.filter(pjname=(form.data)['pjname'],rancher_url__contains="feiyan.com").first()).pjid)
            elif form.tag == "ioc":
                newUrl = (Action.url).format((ProjectService.objects.filter(pjname=(form.data)['pjname'],rancher_url__contains="ioc.com").first()).pjid)
            logger.info(msg=str(kwargs))

            kwargs["headers"]["Authorization"] = Action.token
            kwargs["url"] = newUrl
            kwargs['data'] = json.dumps(svc)
            res = RequestApiAgent().create(**kwargs)
            logger.info(msg="#####rancher create deployment call:###### " + str(res.status_code))
            red = json.loads(res.content)
            logger.info(msg="#####rancher create deployment call:###### " + str(red))
            if res.status_code != 201:
                logger.error(msg="#####rancher create deployment call:###### " + str(red))
                return json_response(error="重新部署rancher deployment api 出现异常，请重试一次！如还有问题请联系运维！")

            kwargs = {
                "url": newUrl + "/"+ "deployment:" + (form.data)['namespaceId'] + ":" + (form.data)['name'],
                "headers": {"Authorization":  Action.token, "Content-Type": "application/json"}
            }
            logger.info(msg=str(kwargs))
            res = RequestApiAgent().list(**kwargs)
            logger.info(msg=str(res.content))
            if res.status_code != 200:
                logger.error(msg="#####rancher create deployment call:###### " + str(res))
                return json_response(error="获取rancher deployment api 出现异常，请重试一次！如还有问题请联系运维！")

            logger.info(msg="##get deployment api start###")
            red = json.loads(res.content)
            logger.info(msg=str(red))
            tmpenv= []
            if red['containers'][0].get('environment'):
                tmpenv.append(red['containers'][0].get('environment'))


            rurl = ""
            vfurl = ""
            if form.tag == "ioc" :
                rurl = "https://rancher.ioc.com/"
                vfurl = "https://rancher.ioc.com/p/" + red['projectId'] + "/workload/" + red['id']
            elif form.tag == "feiyan":
                rurl = "https://rancher.feiyan.com/"
                vfurl = "https://rancher.feiyan.com/p/"+ red['projectId'] + "/workload/" + red['id']
            elif form.tag == "feiyanuos":
                rurl ="https://rancher.feiyan.uos.com/"
                vfurl = "https://rancher.feiyan.uos.com/p/"+ red['projectId'] + "/workload/" + red['id']


            m = ProjectService.objects.create(
                top_project=(ProjectService.objects.filter(pjid=red['projectId']).first()).top_project,
                toppjid=(ProjectService.objects.filter(pjid=red['projectId']).first()).toppjid,
                pjname=(ProjectService.objects.filter(pjid=red['projectId']).first()).pjname,
                pjid=red['projectId'],
                nsname=red['namespaceId'],
                nsid=red['namespaceId'],
                dpname=red['name'],
                dpid=red['id'],
                img=red['containers'][0]['image'],
                replica=red['scale'],
                rancher_url= rurl,
                state=red['state'],
                pubsvc=red.get('publicEndpoints',None),
                create_by=request.user,
                env_id=2,
                cbox_env=tmpenv,
                v_mount=red['containers'][0].get('volumeMounts',[]),
                volumes=red.get('volumes',None),
                cports=red['containers'][0].get('ports',[]),
                pauselinks=red['actions']['pause'],
                rdplinks=red['actions']['redeploy'],
                rollbacklinks=red['actions']['rollback'],
                updatelinks=red['links']['update'],
                removelinks=red['links']['remove'],
                revisionslinks=red['links']['revisions'],
                statuslinks=((RancherApiConfig.objects.filter(env_id=form.env, label="GETSVC", tag=form.tag).first()).url).format(red['projectId']) + "/" +red['id'] ,
                verifyurl=vfurl,
            )
            m.save()
            if (form.data)['cmapid'] is not None:
                try:
                    Action = RancherApiConfig.objects.filter(env_id=form.env, label="GETSIGCMAP",tag=form.tag).first()
                    # newUrl = (Action.url).format((ProjectService.objects.filter(pjname=(form.data)['pjname']).first()).pjid,(form.data)['cmapid'])
                    newUrl = (Action.url).format(red['projectId'],(form.data)['cmapid'])
                    kwargs = {
                        "url": newUrl,
                        "headers": {"Authorization": Action.token, "Content-Type": "application/json"}
                    }
                    logger.info(msg="####svc configmap args######")
                    logger.info(msg=str(kwargs))
                    cres = RequestApiAgent().list(**kwargs)
                    cred = json.loads(cres.content)
                    logger.info(msg=str(cred))
                    kvtmp = []
                    if cred.get("data",None):
                        for k,v in dict.items(cred["data"]):
                            kvtmp.append({"k":k,"v":v})

                    ProjectService.objects.filter(pjid=red['projectId'],dpid=red['id']).update(configId=cred['id'],configName=cred['name'], configMap=kvtmp)
                except Exception as e:
                    logger.error(msg="###svc cmap save error ->>>>>>>"+str(e))

            LoggerOpRecord.objects.create(create_by=request.user,content="CreatePod:" +red['name']+str(request.user.nickname),action="create")
            logger.info(msg="#####rancher create deployment done###### ")


        return json_response(error=error)



class RancherRollbackView(View):
    def get(self,request,id):
        if RancherSvcPubStandby.objects.filter(app_id=id).exists():
            try:
                t = RancherSvcPubStandby.objects.filter(app_id=id).first()
                global tt
                if (t.revisionslinks).find("ioc.com")>-1:
                    tt="ioc"
                elif (t.revisionslinks).find("feiyan.com")>-1:
                    tt="feiyan"
                elif (t.revisionslinks).find("feiyan.uos.com")>-1:
                    tt="feiyanuos"
                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag=tt).first()
                kwargs = {
                    "url": t.revisionslinks,
                    "headers": {"Authorization": "", "Content-Type": "application/json"}
                }
                kwargs["headers"]["Authorization"] = Action.token
                res = RequestApiAgent().list(**kwargs)
                red = (json.loads(res.content))['data']
                return json_response({"data": red})
            except Exception as e :
                logger.error("获取回滚版本失败->"+ str(e))
        return json_response(error="该应用无法获取回滚版本")


    def post(self, request,id):
        form, error = JsonParser(
            Argument('data', required=True,type=dict, help='replicaSetId'),
        ).parse(request.body)
        if error is None:
            if RancherSvcPubStandby.objects.filter(app_id=id).exists():
                t = RancherSvcPubStandby.objects.get(app_id=id)
                global tt
                if (t.revisionslinks).find("ioc.com")>-1:
                    tt="ioc"
                elif (t.revisionslinks).find("feiyan.com")>-1:
                    tt="feiyan"
                elif (t.revisionslinks).find("feiyan.uos.com")>-1:
                    tt="feiyanuos"
                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag=tt).first()
                kwargs = {
                    "url": t.rollbacklinks,
                    "headers": {"Authorization": "", "Content-Type": "application/json"}
                }
                kwargs["headers"]["Authorization"] = Action.token
                kwargs["data"] = json.dumps(form.data)
                res = RequestApiAgent().create(**kwargs)
                if res.status_code != 200:
                   return json_response(error="回滚失败")

                ts = ProjectService.objects.get(id=t.service_id)
                tt = ts.to_dict()
                del tt["id"]
                RancherPublishHistory.objects.create(service_id=t.service_id, **tt)

                ProjectService.objects.filter(id=t.service_id).update(img=t.img,configMap=t.configMap)

                LoggerOpRecord.objects.create(create_by=request.user,
                                              content="rollbackPod:" + str(t.dpname) + str(request.user.nickname),
                                              action="rollback")
                return json_response(error=error)

        return json_response(error="回滚资源不存在")

class RancherSvcRestartView(View):
    def post(self, request,):
        form, error = JsonParser(
            Argument('id', required=True,type=int, help='rdpid'),
            Argument('tag', required=True, type=str, help='tag'),
        ).parse(request.body)
        if error is None:
            if ProjectService.objects.filter(pk=form.id).exists():
                t = ProjectService.objects.filter(pk=form.id).first()
                global tt
                if (t.revisionslinks).find("ioc.com")>-1:
                    tt="ioc"
                elif (t.revisionslinks).find("feiyan.com")>-1:
                    tt="feiyan"
                elif (t.revisionslinks).find("feiyan.uos.com")>-1:
                    tt="feiyanuos"

                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag=tt).first()
                kwargs = {
                    "url": t.rdplinks,
                    "headers": {"Authorization": "", "Content-Type": "application/json"}
                }
                kwargs["headers"]["Authorization"] = Action.token
                res = RequestApiAgent().create(**kwargs)
                if res.status_code != 200:
                   return json_response(error="重启失败")
                ProjectService.objects.filter(id=form.id).update(modify_time=datetime.now())
                LoggerOpRecord.objects.create(create_by=request.user,content="restart:"+str(t.id)+":"+t.dpname,action="restart")
                return json_response(error=None)
        return json_response(error="重启资源不存在")


class RancherSvcVersionView(View):
    def get(self,request,id):
        if RancherPublishHistory.objects.filter(service_id=id).exists():
            try:
                data = RancherPublishHistory.objects.filter(service_id=id).all()
                return json_response({"data":  [x.to_dict() for x in data]})
            except Exception as e :
                logger.error("获取回滚版本失败->"+ str(e))
        return json_response(error="无历史版本")
