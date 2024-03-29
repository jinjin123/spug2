# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.views.generic import View
from django.db.models import F
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django_redis import get_redis_connection
import traceback
from django.db.models import Q
from apps.schedule.models import Task
from apps.config.models import RancherApiConfig
from libs import json_response, JsonParser, Argument, human_datetime, human_time, RequestApiAgent,cmapargs
from apps.deploy.models import DeployRequest
from apps.app.models import *
from apps.deploy.utils import deploy_dispatch, Helper
from apps.account.models import User
from apps.host.models import Host
from collections import defaultdict
from threading import Thread
from datetime import datetime
from apps.app.tasks import send_mail_task,patch_task
from django.core.cache import cache
import ast
import subprocess
import json
import uuid
import os
import logging
from apps.message.models import LoggerOpRecord




logger = logging.getLogger('spug_log')



class RequestView(View):
    def get(self, request):
        data, query = [], {}
        # if not request.user.is_supper:
        #     query['deploy__approve_by_id'] = request.user.id
        #     perms = request.user.deploy_perms
        #     query['deploy__approve_by__in__'] = perms['apps']
        query['deploy__env_id__in'] = [1,2]
        for item in DeployRequest.objects.filter(**query).annotate(
                env_id=F('deploy__env_id'),
                env_name=F('deploy__env__name'),
                app_id=F('deploy__app_id'),
                app_name=F('deploy__app__name'),
                app_host_ids=F('deploy__host_ids'),
                app_extend=F('deploy__extend'),
                created_by_user=F('created_by__nickname'),
                pub_tag=F('deploy__pub_tag')):

            tmp = item.to_dict()
            tmp['env_id'] = item.env_id
            tmp['env_name'] = item.env_name
            tmp['app_id'] = item.app_id
            tmp['app_name'] = item.app_name
            tmp['app_extend'] = item.app_extend
            tmp['extra'] = json.loads(item.extra)
            tmp['host_ids'] = json.loads(item.host_ids)
            tmp['app_host_ids'] = json.loads(item.app_host_ids)
            tmp['status_alias'] = item.get_status_display()
            tmp['type'] = item.get_type_display()
            tmp['opshandler'] = item.opshandler
            tmp['opsstatus_alias'] = item.get_opsstatus_display()
            tmp['testhandler'] = item.testhandler
            tmp['teststatus_alias'] = item.get_teststatus_display()
            tmp['type'] = item.get_type_display()
            tmp['created_by_user'] = item.created_by_user
            tmp['pub_tag'] = item.pub_tag
            data.append(tmp)
        return json_response(data)

    def post(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('deploy_id', type=int, help='缺少必要参数'),
            Argument('name', help='请输申请标题'),
            Argument('extra', type=list, help='缺少必要参数'),
            Argument('host_ids', type=list, filter=lambda x: len(x), help='请选择要部署的主机'),
            Argument('desc', required=False),
        ).parse(request.body)
        if error is None:
            deploy = Deploy.objects.filter(pk=form.deploy_id).first()
            if not deploy:
                return json_response(error='未找到该发布配置')
            if form.extra[0] == 'tag' and not form.extra[1]:
                return json_response(error='请选择要发布的Tag')
            if form.extra[0] == 'branch' and not form.extra[2]:
                return json_response(error='请选择要发布的分支及Commit ID')
            if deploy.extend == '2':
                if form.extra[0]:
                    form.extra[0] = form.extra[0].replace("'", '')
                if DeployExtend2.objects.filter(deploy=deploy, host_actions__contains='"src_mode": "1"').exists():
                    if len(form.extra) < 2:
                        return json_response(error='该应用的发布配置中使用了数据传输动作且设置为发布时上传，请上传要传输的数据')
                    form.version = form.extra[1].get('path')
            form.name = form.name.replace("'", '')
            form.status = '0' if deploy.is_audit else '1'
            form.extra = json.dumps(form.extra)
            form.host_ids = json.dumps(form.host_ids)
            if form.id:
                req = DeployRequest.objects.get(pk=form.id)
                is_required_notify = deploy.is_audit and req.status == '-1'
                DeployRequest.objects.filter(pk=form.id).update(
                    created_by=request.user,
                    reason=None,
                    **form
                )
            else:
                req = DeployRequest.objects.create(created_by=request.user, **form)
                is_required_notify = deploy.is_audit
            if is_required_notify:
                Thread(target=Helper.send_deploy_notify, args=(req, 'approve_req')).start()
        return json_response(error=error)

    def put(self, request):
        form, error = JsonParser(
            Argument('id', type=int, help='缺少必要参数'),
            Argument('action', filter=lambda x: x in ('check', 'do'), help='参数错误')
        ).parse(request.body)
        if error is None:
            req = DeployRequest.objects.filter(pk=form.id).first()
            if not req:
                return json_response(error='未找到指定发布申请')
            pre_req = DeployRequest.objects.filter(
                deploy_id=req.deploy_id,
                type='1',
                id__lt=req.id,
                version__isnull=False).first()
            if not pre_req:
                return json_response(error='未找到该应用可以用于回滚的版本')
            if form.action == 'check':
                return json_response({'date': pre_req.created_at, 'name': pre_req.name})
            DeployRequest.objects.create(
                deploy_id=req.deploy_id,
                name=f'{req.name} - 回滚',
                type='2',
                extra=pre_req.extra,
                host_ids=req.host_ids,
                status='0' if pre_req.deploy.is_audit else '1',
                desc='自动回滚至该应用的上个版本',
                version=pre_req.version,
                created_by=request.user
            )
        return json_response(error=error)

    def delete(self, request):
        form, error = JsonParser(
            Argument('id', type=int, required=False),
            Argument('expire', required=False),
            Argument('count', type=int, required=False, help='请输入数字')
        ).parse(request.GET)
        if error is None:
            rds = get_redis_connection()
            if form.id:
                DeployRequest.objects.filter(pk=form.id, status__in=('0', '1', '-1')).delete()
                return json_response()
            elif form.count:
                if form.count < 1:
                    return json_response(error='请输入正确的保留数量')
                counter, ids = defaultdict(int), []
                for item in DeployRequest.objects.all():
                    if counter[item.deploy_id] == form.count:
                        ids.append(item.id)
                    else:
                        counter[item.deploy_id] += 1
                count, _ = DeployRequest.objects.filter(id__in=ids).delete()
                if ids:
                    rds.delete(*(f'{settings.REQUEST_KEY}:{x}' for x in ids))
                return json_response(count)
            elif form.expire:
                requests = DeployRequest.objects.filter(created_at__lt=form.expire)
                ids = [x.id for x in requests]
                count, _ = requests.delete()
                if ids:
                    rds.delete(*(f'{settings.REQUEST_KEY}:{x}' for x in ids))
                return json_response(count)
            else:
                return json_response(error='请至少使用一个删除条件')
        return json_response(error=error)

class RancherPublishView(View):
    def post(self,request):
        form, error = JsonParser(
            Argument('app_id',  help='app_id'),
            Argument('app_name', help='请输申请应用标题'),
            Argument('env_id',type=int,help='环境丢失'),
            Argument('deploy_id', type=int, help='环境丢失'),
            Argument('uniqid', type=int, help='uniqid'),
        ).parse(request.body)
        if error is None:
            kwargs = {
                "url": "",
                "headers": {"Authorization": "", "Content-Type": "application/json"}
            }

            publish_args = (RancherSvcPubStandby.objects.filter(id=form.uniqid,app_id=form.app_id).first()).to_dict()
            try:
                Action = ""
                logger.info(msg="#######redeploy pod start ########")
                if form.env_id == 1:
                    if publish_args['update_img'] : #1 only config update #0 img update
                        Action = RancherApiConfig.objects.filter(env_id=1, label="REDOSVC").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(publish_args['project_id'], publish_args['deployid'])
                        res = RequestApiAgent().create(**kwargs)
                        logger.info(msg="#####rancher redploy dev call:###### " + str(res.status_code))
                        if res.status_code != 200:
                            logger.error(msg="#####rancher redploy dev call:###### " + str(res))
                            return json_response(error="重新部署rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                        DeployRequest.objects.filter(deploy_id=form.deploy_id).update(status=3)
                elif form.env_id == 2:
                    if (publish_args['statuslinks']).find("ioc.com") > -1:
                        Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="ioc").first()
                    elif (publish_args['statuslinks']).find("feiyan.com") > -1:
                        Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="feiyan").first()
                    elif (publish_args['statuslinks']).find("feiyan.uos.com") > -1:
                        Action = RancherApiConfig.objects.filter(env_id=2, label="GETSVC",tag="feiyanuos").first()
                    kwargs["headers"]["Authorization"] = Action.token
                    kwargs["url"] = publish_args['statuslinks']
                    oldres = RequestApiAgent().list(**kwargs)
                    oldcd = json.loads(oldres.content)
                    if not publish_args["update_img"]:
                        if oldcd.get('containers',False):
                            oldcd["containers"][0]['image'] =publish_args['img']
                            kwargs['data'] = json.dumps(oldcd)
                            logger.info(msg="###update pod args ---->"+json.dumps(kwargs))
                            imgres = RequestApiAgent().put(**kwargs)
                            if imgres.status_code != 200:
                                DeployRequest.objects.filter(id=form.uniqid,deploy_id=form.deploy_id).update(status="-3", opsstatus=-3)
                                logger.error(msg="### pubish redeploy rancher ## error->" + str(imgres))
                                return json_response(error="更新应用rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                            logger.info(msg="###update pod done  #####")
                            imgdd = json.loads(imgres.content)

                            ts = ProjectService.objects.get(id=publish_args['service_id'])
                            t = ts.to_dict()
                            del t["id"]
                            RancherPublishHistory.objects.create(service_id=publish_args['service_id'],**t)
                            ProjectService.objects.filter(id=publish_args['service_id']).update(img=imgdd['containers'][0]['image'],modify_time=datetime.now())
                            DeployRequest.objects.filter(id=form.uniqid,deploy_id=form.deploy_id).update(status=3,opsstatus=3)
                            RancherSvcPubStandby.objects.filter(id=form.uniqid,app_id=form.app_id).update(state=1,modify_time=datetime.now())
                            logger.info(msg="###update pod  into db done  #####")
                        else:
                            return json_response(error="数据跟rancher没同步，走Jenkins发布")

                    if not publish_args["update_cmap"]:
                        if (publish_args['statuslinks']).find("ioc.com") > -1:
                            Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="ioc").first()
                        elif (publish_args['statuslinks']).find("feiyan.com") > -1:
                            Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="feiyan").first()
                        elif (publish_args['statuslinks']).find("feiyan.uos.com") > -1:
                            Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="feiyanuos").first()
                        kwargs["headers"]["Authorization"] = Action.token
                        kwargs["url"] = (Action.url).format(publish_args['pjid'], publish_args['configId'])

                        dataargs = cmapargs()
                        dd = {}
                        for x in ast.literal_eval(publish_args['configMap']):
                            dd[x["k"]] = x["v"]
                        dataargs["data"] = dd
                        dataargs["namespaceId"] = publish_args["nsid"]
                        dataargs["id"] = publish_args["configId"]

                        kwargs['data'] = json.dumps(dataargs)
                        logger.info(msg="###update cmap args ---->"+json.dumps(kwargs))

                        cres = RequestApiAgent().put(**kwargs)
                        cred = json.loads(cres.content)

                        if cres.status_code != 200:
                            DeployRequest.objects.filter(deploy_id=form.deploy_id).update(status="-3", opsstatus=-3)
                            logger.error(msg="#####rancher update  configmap call:###### " + json.dumps(cred))
                            return json_response(error="更新应用rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                        try:
                            if (publish_args['statuslinks']).find("ioc.com") > -1:
                                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="ioc").first()
                            elif (publish_args['statuslinks']).find("feiyan.com") > -1:
                                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="feiyan").first()
                            elif (publish_args['statuslinks']).find("feiyan.uos.com") > -1:
                                Action = RancherApiConfig.objects.filter(env_id=2, label="GETSIGCMAP",tag="feiyanuos").first()
                            kwargs["headers"]["Authorization"] = Action.token
                            kwargs["url"] =  publish_args['rdplinks']
                            rdp = RequestApiAgent().create(**kwargs)
                            if rdp.status_code != 200:
                                DeployRequest.objects.filter(deploy_id=form.deploy_id).update(status="-3",opsstatus=-3)
                                logger.error(msg="### pubish redeploy rancher ## error->"+ str(rdp) )
                                return json_response(error="更新应用rancher api 出现异常，请重试一次！如还有问题请联系运维！")

                        except Exception as e :
                            print(e)
                            traceback.print_exc()
                            DeployRequest.objects.filter(deploy_id=form.deploy_id).update(status="-3", opsstatus=-3)
                            logger.error(msg="### pubish redeploy rancher ## error->"+ str(e))
                            return json_response(error="更新应用rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                        kvtmp = []
                        if cred.get('data',False):
                            for k,v in dict.items(cred["data"]):
                                kvtmp.append({"k":k,"v":v})

                            ProjectConfigMap.objects.filter(pjid=cred['projectId'],nsid=cred['namespaceId'],configId=cred['id'],configName=cred['name']).update(configMap=kvtmp,modify_time=datetime.now())
                            logger.info(msg="###update cmap done ####")
                            ts = ProjectService.objects.get(id=publish_args['service_id'])
                            t = ts.to_dict()
                            del t["id"]
                            RancherPublishHistory.objects.create(service_id=publish_args['service_id'],**t)
                            ProjectService.objects.filter(id=publish_args['service_id']).update(configMap=kvtmp,modify_time=datetime.now())
                            DeployRequest.objects.filter(id=form.uniqid,deploy_id=form.deploy_id).update(status=3,opsstatus=3)
                            RancherSvcPubStandby.objects.filter(id=form.uniqid,app_id=form.app_id).update(state=1,modify_time=datetime.now())
                        else:
                            ProjectConfigMap.objects.filter(pjid=cred['projectId'],nsid=cred['namespaceId'],configId=cred['id'],configName=cred['name']).update(configMap=kvtmp,modify_time=datetime.now())
                            logger.info(msg="###update cmap done ####")
                            ts = ProjectService.objects.get(id=publish_args['service_id'])
                            t = ts.to_dict()
                            del t["id"]
                            RancherPublishHistory.objects.create(service_id=publish_args['service_id'],**t)
                            ProjectService.objects.filter(id=publish_args['service_id']).update(configName="", configId="",configMap=kvtmp,modify_time=datetime.now())
                            DeployRequest.objects.filter(id=form.uniqid,deploy_id=form.deploy_id).update(status=3,opsstatus=3)
                            RancherSvcPubStandby.objects.filter(id=form.uniqid,app_id=form.app_id).update(state=1,modify_time=datetime.now())
                            logger.info(msg="configmap not get data svcid-->"+ str(publish_args['service_id']))

                    ##### after rdp
                    kwargs = {
                        "url": "",
                        "headers": {"Authorization": "", "Content-Type": "application/json"}
                    }
                    kwargs["headers"]["Authorization"] = Action.token
                    kwargs["url"] = publish_args['rdplinks']
                    res = RequestApiAgent().create(**kwargs)
                    logger.info(msg="#####rancher redploy prod call:###### " + str(res.status_code))
                    if res.status_code != 200:
                        logger.error(msg="#####rancher redploy prod call:###### " + str(res))
                        return json_response(error="重新部署rancher api 出现异常，请重试一次！如还有问题请联系运维！")
                    # DeployRequest.objects.filter(deploy_id=form.deploy_id).update(status=3)
                    logger.info(msg="#######redeploy pod done ########")

            except Exception as  e:
                print(e)
                traceback.print_exc()
                logger.error(msg="#######redeploy pod faild: ########" + str(e))
                return json_response(error=str(e))
        return json_response(error=error)


class RequestRancherDeployView(View):
    def post(self, request):
        form, error = JsonParser(
            Argument('app_name',  help='app_name',required=True),
            Argument('dpname',  help='deployname',required=False),
            Argument('dpid',  help='dpid',required=False),
            Argument('cbox_env',  help='cbox_env',required=False),
            Argument('configId',  help='configId',required=False),
            Argument('configMap', help='configMap',required=False),
            Argument('configName', help='configName',required=False),
            # Argument('create_by', help='create_by',required=False),
            Argument('developer', help='developer',required=False),
            Argument('opsper', help='opsper',required=False),
            Argument('env_id', help='env_id',required=False),
            Argument('img', help='img',required=False),
            Argument('nsid', help='nsid',required=False),
            Argument('nsname', help='nsname',required=False),
            Argument('is_audit', help='is_audit',required=False),
            Argument('pbtype', help='pbtype',required=False),
            Argument('pjid', help='pjid',required=False),
            Argument('pjname', help='pjname',required=False),
            Argument('pubsvc', help='pubsvc',required=False),
            Argument('rancher_url', help='rancher_url',required=False),
            Argument('replica', help='replica',required=False),
            Argument('state', help='state',required=False),
            Argument('top_project', help='top_project',required=False),
            Argument('toppjid', help='toppjid',required=False),
            Argument('update_img', help='update_img',required=False),
            Argument('update_cmap', help='update_cmap',required=False),
            Argument('v_mount', help='v_mount',required=False),
            Argument('verifyurl', help='verifyurl',required=False),
            Argument('volumes', help='volumes',required=False),

            Argument('rollbacklinks', help='rollbacklinks', required=False),
            Argument('statuslinks', help='statuslinks', required=False),
            Argument('updatelinks', help='updatelinks', required=False),
            Argument('rollbacklinks', help='rollbacklinks', required=False),
            Argument('revisionslinks', help='revisionslinks', required=False),
            Argument('rdplinks', help='rdplinks', required=False),
            Argument('pauselinks', help='pauselinks', required=False),
            Argument('removelinks', help='removelinks', required=False),
            Argument('cports', help='cports', required=False),
            Argument('desccomment', help='desccomment', required=False),
            Argument('trigger', filter=lambda x: x in dict(Task.TRIGGERS), help='请选择触发器类型'),
            Argument('trigger_args', help='请输入触发器参数'),
        ).parse(request.body)
        if error is None:
            try:
                if App.objects.filter(key=form.app_name).exists():
                    return json_response(error="申请发布标题唯一命名已存在")
                deploy_app = App.objects.filter(name=form.dpname,key=form.app_name).first()
                global  ap,d
                if not deploy_app :
                    ap = App.objects.create(
                        name=form.dpname,
                        key=form.app_name,
                        created_by=request.user
                    )
                    ap.save()
                deploy = Deploy.objects.filter(app=App.objects.filter(name=form.dpname,key=form.app_name).first()).first()
                if not deploy :
                    d = Deploy.objects.create(
                        app=App.objects.filter(name=form.dpname,key=form.app_name).first(),
                        env_id=form.env_id,
                        host_ids=[],
                        is_audit=1,
                        extend=2,
                        rst_notify='{"mode": "0"}',
                        created_by=request.user,
                        pub_tag=2
                    )
                    d.save()
                dr = DeployRequest.objects.create(
                    created_by=request.user,
                    name=form.app_name,
                    type=form.pbtype,
                    extra='[null]',
                    host_ids='[]',
                    status=0,
                    deploy=Deploy.objects.filter(app=App.objects.filter(name=form.dpname,key=form.app_name).first()).first(),
                    desccomment=form.desccomment,
                    trigger_args=form.trigger_args
                )
                dr.save()
                Task.objects.create(
                    command=json.dumps({"app_id":ap.id, "uniqid": dr.id,"app_name": form.app_name,"env_id": 2,"deploy_id": d.id }),
                    tag="rancher",
                    name=form.app_name,
                    rst_notify=json.dumps({"mode":"0"}),
                    targets=json.dumps(["local"]),
                    trigger=form.trigger,
                    trigger_args=form.trigger_args,
                    type="TEST",
                    is_active=False,
                    created_by=request.user
                )

                tmptrigger = form.pop("trigger")
                tmptrigger_args = form.pop("trigger_args")
                tmpdes = form.pop("desccomment")
                m = RancherSvcPubStandby.objects.create(
                    create_by=request.user,
                    app=App.objects.filter(key=form.pop('app_name')).first(),
                    service=ProjectService.objects.filter(top_project=form.top_project,dpname=form.dpname,dpid=form.dpid).first(),
                    **form
                )
                m.save()
                patch_task.delay()
                mobj = RancherSvcPubStandby.objects.get(id=m.id)
                if ProjectServiceApprovalNotice.objects.filter(service_id=mobj.service_id).exists():
                    notice = ProjectServiceApprovalNotice.objects.filter(service_id=mobj.service_id).exclude(email__isnull=True).values("notice_user__email").all()
                    to_email=[ item["notice_user__email"] for item in notice]
                    send_mail_task.delay(subject="%s-%s应用发布审核申请"%(form.top_project,form.dpname), content="申请人:{} \n{}项目\n{}应用发布审核申请\n发布功能:\n{}\n查看 {}".format(request.user.nickname,form.top_project,form.dpname,tmpdes,form.verifyurl),
                                         from_mail=settings.DEFAULT_FROM_EMAIL,to_email=",".join(to_email))
                else:
                    to_email = [item["email"] for item in User.objects.filter(role_id=1).exclude(email__isnull=True).values("email").all()]
                    send_mail_task.delay(subject="%s-%s应用发布审核申请" % (form.top_project, form.dpname),
                                     content="申请人:{}\n{}项目\n{}应用发布审核申请\n发布功能:\n{}\n查看 {}".format(request.user.nickname,form.top_project, form.dpname,tmpdes,form.verifyurl),
                                     from_mail=settings.DEFAULT_FROM_EMAIL, to_email=",".join(to_email))


            except Exception as e:
                print(e)
                logger.error(msg="auth order  create error->"+str(traceback.format_exc()))
            #----
            # for item in pblist:
            #     if ProjectServiceApprovalNotice.objects.filter(service_id=item.service_id).first():
            #         notice = ProjectServiceApprovalNotice.objects.filter(service_id=item.service_id).values("notice_user__email").all()
            #         to_email=[ item["notice_user__email"] for item in notice]
            #         send_mail_task.delay(subject="%s-%s应用发布审核申请"%(form.top_project,form.dpname), content="申请人:{} \n{}项目\n{}应用发布审核申请\n发布功能:\n{}\n查看 {}".format(request.user.nickname,form.top_project,form.dpname,tmpdes,form.verifyurl),
            #                              from_mail=settings.DEFAULT_FROM_EMAIL,to_email=",".join(to_email))
            #     else:
            #         to_email = [item["email"] for item in User.objects.filter(role_id=1).values("email").all()]
            #         send_mail_task.delay(subject="%s-%s应用发布审核申请" % (form.top_project, form.dpname),
            #                          content="申请人:{}\n{}项目\n{}应用发布审核申请\n发布功能:\n{}\n查看 {}".format(request.user.nickname,form.top_project, form.dpname,tmpdes,form.verifyurl),
            #                          from_mail=settings.DEFAULT_FROM_EMAIL, to_email=",".join(to_email))

        return json_response(error=error)




class RequestDetailView(View):
    def get(self, request,envid, r_id):
        req = DeployRequest.objects.filter(pk=r_id).first()
        if not req:
            return json_response(error='未找到指定发布申请')
        d = DeployRequest.objects.get(pk=r_id)
        r = RancherSvcPubStandby.objects.filter(app_id=Deploy.objects.get(pk=d.deploy_id).app_id).first()
        Action =""
        if (r.statuslinks).find("ioc.com") > -1:
            Action = RancherApiConfig.objects.filter(env_id=envid, label="GETSVC", tag="ioc").first()
        elif (r.statuslinks).find("feiyan.com") > -1:
            Action = RancherApiConfig.objects.filter(env_id=envid, label="GETSVC", tag="feiyan").first()
        elif (r.statuslinks).find("feiyan.uos.com") > -1:
            Action = RancherApiConfig.objects.filter(env_id=envid, label="GETSVC", tag="feiyanuos").first()
        kwargs = {
            "url": r.statuslinks,
            "headers": {"Authorization": "", "Content-Type": "application/json"}
        }
        kwargs["headers"]["Authorization"] = Action.token
        res = RequestApiAgent().list(**kwargs)
        if res.status_code != 200:
            logger.error(msg="rancher结果返回失败->>>>"+str(res.content))
            return json_response(error="rancher结果返回失败")
        tlink = r.rancher_url + "p/"+ r.pjid + '/workload/'+ r.dpid
        red = json.loads(res.content)
        return json_response({"data":red,"tlink":tlink})


        # hosts = Host.objects.filter(id__in=json.loads(req.host_ids))
        # targets = [{'id': x.id, 'title': f'{x.name}({x.hostname}:{x.port})'} for x in hosts]
        # server_actions, host_actions, outputs = [], [], []
        # if req.deploy.extend == '2':
        #     server_actions = json.loads(req.deploy.extend_obj.server_actions)
        #     host_actions = json.loads(req.deploy.extend_obj.host_actions)
        # if request.GET.get('log'):
        #     rds, key, counter = get_redis_connection(), f'{settings.REQUEST_KEY}:{r_id}', 0
        #     data = rds.lrange(key, counter, counter + 9)
        #     while data:
        #         counter += 10
        #         outputs.extend(x.decode() for x in data)
        #         data = rds.lrange(key, counter, counter + 9)
        # return json_response({
        #     'app_name': req.deploy.app.name,
        #     'env_name': req.deploy.env.name,
        #     'status': req.status,
        #     'type': req.type,
        #     'status_alias': req.get_status_display(),
        #     'targets': targets,
        #     'server_actions': server_actions,
        #     'host_actions': host_actions,
        #     'outputs': outputs
        # })

    def post(self, request, r_id):
        query = {'pk': r_id}
        if not request.user.is_supper:
            perms = request.user.deploy_perms
            query['deploy__app_id__in'] = perms['apps']
            query['deploy__env_id__in'] = perms['envs']
        req = DeployRequest.objects.filter(**query).first()
        if not req:
            return json_response(error='未找到指定发布申请')
        if req.status not in ('1', '-3'):
            return json_response(error='该申请单当前状态还不能执行发布')
        hosts = Host.objects.filter(id__in=json.loads(req.host_ids))
        token = uuid.uuid4().hex
        outputs = {str(x.id): {'data': []} for x in hosts}
        outputs.update(local={'data': [f'{human_time()} 建立接连...        ']})
        req.status = '2'
        req.do_at = human_datetime()
        req.do_by = request.user
        if not req.version:
            req.version = f'{req.deploy_id}_{req.id}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        req.save()
        Thread(target=deploy_dispatch, args=(request, req, token)).start()
        return json_response({'token': token, 'type': req.type, 'outputs': outputs})

    def patch(self, request,envid, r_id):
        form, error = JsonParser(
            Argument('reason', required=False),
            Argument('author', required=False),
            Argument('is_pass', type=bool, help='参数错误')
        ).parse(request.body)
        if error is None:
            req = DeployRequest.objects.filter(pk=r_id).first()
            if not req:
                return json_response(error='未找到指定申请')
            if not form.is_pass and not form.reason:
                return json_response(error='请输入驳回原因')
            # if req.status != '0':
            #     return json_response(error='该申请当前状态不允许审核')
            req.approve_at = human_datetime()
            req.approve_by = request.user
            if form.author == "ops":
                req.status = '1' if form.is_pass else '-1'
                req.opsstatus = 1 if form.is_pass else -1
                req.opshandler = request.user.nickname
            elif form.author == "test":
                req.status = '3' if form.is_pass else '-3'
                req.teststatus = 3 if form.is_pass else -3
                req.testhandler = request.user.nickname
            req.reason = form.reason
            req.save()
            Thread(target=Helper.send_deploy_notify, args=(req, 'approve_rst')).start()
        return json_response(error=error)

    def delete(self,request,envid, r_id ):
        if r_id:
            try:
                logger.info(msg="del approval  start----->")
                if DeployRequest.objects.filter(id=r_id).exists():
                    m = DeployRequest.objects.get(id=r_id)
                    m.delete()
                    d = RancherSvcPubStandby.objects.get(id=r_id)
                    d.delete()
                    logger.info(msg="del approval  done----->")
                    LoggerOpRecord.objects.create(create_by=request.user,
                            content="del approval:" + str(r_id) + ":" + d.dpname, action="del")

                    return json_response(error=None)
                else:
                    return json_response(error="已经删除/记录不存在,刷新一下")
            except Exception as e :
                logger.error(msg="del approval  err----->"+ str(e))


def do_upload(request):
    repos_dir = settings.REPOS_DIR
    file = request.FILES['file']
    deploy_id = request.POST.get('deploy_id')
    if file and deploy_id:
        dir_name = os.path.join(repos_dir, deploy_id)
        file_name = datetime.now().strftime("%Y%m%d%H%M%S")
        command = f'mkdir -p {dir_name} && cd {dir_name} && ls | sort  -rn | tail -n +11 | xargs rm -rf'
        code, outputs = subprocess.getstatusoutput(command)
        if code != 0:
            return json_response(error=outputs)
        with open(os.path.join(dir_name, file_name), 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return json_response(file_name)
    else:
        return HttpResponseBadRequest()


# def create_email_message(subject, content, to_mail=None, from_mail=settings.DEFAULT_FROM_EMAIL, send=True):
    # message = EmailRecord.objects.create(
    #     to_email=to_mail,
    #     from_email=from_mail,
    #     subject=subject,
    #     content=content,
    # )
    # from django.core import serializers
    # messageobj = serializers.serialize('json', message)
    # if send:
    #     send_mail_task.delay()

class RequestChangeDetailView(View):
    def get(self, request, id):
        if RancherSvcPubStandby.objects.filter(app_id=id).exists():
            t = RancherSvcPubStandby.objects.filter(app_id=id).first()
            old = ProjectService.objects.get(pk=t.service_id)
            tmp = []
            oldtmp = []
            for x in ast.literal_eval(t.configMap):
                tmp.append({x["k"]:x["v"]})
            for x in ast.literal_eval(old.configMap):
                oldtmp.append({x["k"]:x["v"]})

            if t.update_img == 0 and t.update_cmap == 0:
                return json_response({"data": [{"img":t.img,"cmap":tmp,"tag":"new"},{"img":old.img, "cmap":oldtmp,"tag":"old"}], "update_img": t.update_img,"update_cmap": t.update_cmap })
            elif t.update_img == 0:
                return json_response({"data": [{"img":t.img,"tag":"new"},{"img":old.img, "tag":"old"}], "update_img": t.update_img ,"update_cmap": t.update_cmap})
            elif t.update_cmap == 0:
                return json_response({"data": [{"cmap":tmp,"tag":"new"},{"cmap":oldtmp,"tag":"old"}], "update_cmap": t.update_cmap,"update_img": t.update_img})

        return json_response(error='无变动')

class RequestMaster(View):
    def post(self,request):
        m = cache.get("tmpmaster",[])
        if len(m) == 0 :
            tmp = []
        else:
            tmp = m
        tmp.append(request.user.id)
        try:
            User.objects.filter(id=request.user.id).update(role_id=1)
            request.user.token_expired = 0
            cache.set("tmpmaster", tmp,500*10000)
            LoggerOpRecord.objects.create(create_by=request.user, content="BootsMaster:" + str(request.user.nickname),
                                          action="updateauth")
        except Exception as e:
            logger.error(msg="save tmp authmaster error------->"+ str(e))
            return json_response(error="提权失败")
        return json_response(error=None)


class RequestOplog(View):
    def get(self,request):
        m = LoggerOpRecord.objects.all()

        return json_response({"data": [x.to_dict() for x in m ]})
