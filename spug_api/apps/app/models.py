# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin, human_datetime
from apps.account.models import User
from apps.config.models import Environment
import json
from django_mysql.models.fields import SizedTextField
import ast


class App(models.Model, ModelMixin):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=255, null=True)
    rel_apps = models.TextField(null=True)
    rel_services = models.TextField(null=True)
    sort_id = models.IntegerField(default=0, db_index=True)
    created_at = models.CharField(max_length=20, default=human_datetime)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['rel_apps'] = json.loads(self.rel_apps) if self.rel_apps else []
        tmp['rel_services'] = json.loads(self.rel_services) if self.rel_services else []
        return tmp

    def __repr__(self):
        return f'<App {self.name!r}>'

    class Meta:
        db_table = 'apps'
        ordering = ('-sort_id',)


class Deploy(models.Model, ModelMixin):
    EXTENDS = (
        ('1', '常规发布'),
        ('2', '自定义发布'),
    )
    PUBTAG = (
        ('1', '主机发布'),
        ('2', 'rancher发布'),
    )
    app = models.ForeignKey(App, on_delete=models.PROTECT)
    env = models.ForeignKey(Environment, on_delete=models.PROTECT)
    host_ids = models.TextField()
    extend = models.CharField(max_length=2, choices=EXTENDS)
    is_audit = models.BooleanField()
    rst_notify = models.CharField(max_length=255, null=True)

    created_at = models.CharField(max_length=20, default=human_datetime)
    created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    updated_at = models.CharField(max_length=20, null=True)
    updated_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)
    pub_tag = models.CharField(max_length=2, choices=PUBTAG)

    @property
    def extend_obj(self):
        cls = DeployExtend1 if self.extend == '1' else DeployExtend2
        return cls.objects.filter(deploy=self).first()

    def to_dict(self, *args, **kwargs):
        deploy = super().to_dict(*args, **kwargs)
        deploy['app_name'] = self.app_name if hasattr(self, 'app_name') else None
        deploy['host_ids'] = json.loads(self.host_ids)
        deploy['rst_notify'] = json.loads(self.rst_notify)
        deploy.update(self.extend_obj.to_dict())
        return deploy

    def __repr__(self):
        return '<Deploy app_id=%r>' % self.app_id

    class Meta:
        db_table = 'deploys'
        ordering = ('-id',)


class DeployExtend1(models.Model, ModelMixin):
    deploy = models.OneToOneField(Deploy, primary_key=True, on_delete=models.CASCADE)
    git_repo = models.CharField(max_length=255)
    dst_dir = models.CharField(max_length=255)
    dst_repo = models.CharField(max_length=255)
    versions = models.IntegerField()
    filter_rule = models.TextField()
    custom_envs = models.TextField()
    hook_pre_server = models.TextField(null=True)
    hook_post_server = models.TextField(null=True)
    hook_pre_host = models.TextField(null=True)
    hook_post_host = models.TextField(null=True)

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['filter_rule'] = json.loads(self.filter_rule)
        tmp['custom_envs'] = '\n'.join(f'{k}={v}' for k, v in json.loads(self.custom_envs).items())
        return tmp

    def __repr__(self):
        return '<DeployExtend1 deploy_id=%r>' % self.deploy_id

    class Meta:
        db_table = 'deploy_extend1'


class DeployExtend2(models.Model, ModelMixin):
    deploy = models.OneToOneField(Deploy, primary_key=True, on_delete=models.CASCADE)
    server_actions = models.TextField()
    host_actions = models.TextField()

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['server_actions'] = json.loads(self.server_actions)
        tmp['host_actions'] = json.loads(self.host_actions)
        return tmp

    def __repr__(self):
        return '<DeployExtend2 deploy_id=%r>' % self.deploy_id

    class Meta:
        db_table = 'deploy_extend2'


# class CMDB(models.Model, ModelMixin):
#     STATUS_CHOOSE = (
#         ('Y', 'up'),
#         ('N', 'down'),
#     )
#     top_project = models.CharField(max_length=128, verbose_name="顶级项目", null=True)
#     top_projectid = models.CharField(max_length=100, verbose_name="顶级项目id", null=True)
#     ipaddress = models.CharField(max_length=15, verbose_name="ip", null=True)
#     service_pack = models.CharField(max_length=500, verbose_name="包含哪些服务类型包'',''", null=True)
#     osType = models.CharField(max_length=155,verbose_name='系统类型', null=True)
#     osVerion = models.CharField(max_length=100,verbose_name='发行版本', null=True)
#     coreVerion = models.CharField(max_length=100,verbose_name='内核版本', null=True)
#     disks_format = models.CharField(max_length=255,verbose_name='数据盘格式', null=True)
#     disks = models.IntegerField(verbose_name='数据盘数量', null=True)
#     disks_capacity = models.CharField(max_length=255, verbose_name="数据盘容量'',''", null=True)
#     memory = models.IntegerField(verbose_name='内存GB', null=True)
#     cpus = models.IntegerField(default=0, verbose_name='cpu数量', null=True)
#     cpucore = models.IntegerField(default=0, verbose_name='cpu物理核', null=True)
#     serial_num = models.CharField(verbose_name='序列号', max_length=100, null=True)
#     status = models.CharField(choices=STATUS_CHOOSE, default='Y', verbose_name='同步监控状态(关机释放下线)', null=True)
#     host_name = models.CharField(max_length=100, verbose_name='主机名', null=True)
#     supplier = models.CharField(max_length=100, verbose_name='供应商', null=True)
#     host_bug = models.CharField(max_length=500, verbose_name='服务版本与是否打补丁['','']', null=True)
#     ext_config1 = models.CharField(max_length=255, verbose_name='扩展信息', null=True)
#     developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
#     opsper = models.CharField(max_length=200, verbose_name='运维负责人' ,null=True)
#     zone = models.CharField(max_length=50,verbose_name="分组", null=True)
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
#     create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
#     env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)

class ProjectService(models.Model, ModelMixin):
    top_project = models.CharField(max_length=200, verbose_name="所属顶级项目")
    toppjid = models.CharField(max_length=200, verbose_name="所属顶级项目id")
    pjname = models.CharField(db_index=True, max_length=80, verbose_name='rancher项目名称唯一', null=True)
    pjid = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    nsname = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    nsid = models.CharField(max_length=50, verbose_name='ranchernamespaceid唯一', null=True)
    dpname = models.CharField(max_length=80, db_index=True, verbose_name='部署服务名称(在rancher下必须唯一)', null=True)
    dpid = models.CharField(max_length=80, db_index=True, verbose_name='发布部署app唯一', null=True)
    img = models.CharField(max_length=255, verbose_name='部署镜像', null=True)
    replica = models.IntegerField(default=1, db_index=True, verbose_name='pod副本scale伸缩', null=True)
    configId = models.CharField(max_length=200, verbose_name='configId')
    configName = models.CharField(max_length=200, verbose_name='配置映射卷名')
    configMap = SizedTextField(size_class=3, verbose_name='配置映射卷多[{k,v}]', default='[]')
    # pvcid = models.CharField(max_length=200, verbose_name='pvcid')
    # pvcsize = models.CharField(max_length=200, verbose_name='pvc配置映射卷大小')
    rancher_url = models.CharField(max_length=200, verbose_name="rancher前缀url", null=True)
    state = models.CharField(max_length=50, default='Y', verbose_name='同步服务监控状态(关机释放下线)', null=True)
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人',null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    pubsvc = models.CharField(max_length=300, verbose_name='暴露端口与服务所在部署主机地址', null=True)
    v_mount = models.CharField(max_length=1500,verbose_name="挂载详情",null=True)
    volumes = models.CharField(max_length=1500,verbose_name="卷详情",null=True)
    cbox_env = models.CharField(max_length=1500,verbose_name="容器变量",null=True)
    verifyurl = models.CharField(max_length=255,verbose_name='rancher app check',null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    # depends_svc = models.CharField(max_length=500, verbose_name="依赖服务或组件多余注释", null=True)

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        t = []
        for x in ast.literal_eval(self.configMap):
            t.append(x)

        tmp["configMap"] = t
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_service'

class ProjectConfigMap(models.Model, ModelMixin):
    pjid = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    configId = models.CharField(max_length=200, verbose_name='configId')
    configName = models.CharField(max_length=200, verbose_name='配置映射卷名')
    configMap = SizedTextField(size_class=3, verbose_name='配置映射卷多[{k,v}]', default='[]')
    nsname = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    nsid = models.CharField(max_length=50, verbose_name='ranchernamespaceid唯一', null=True)
    dellinks = models.CharField(max_length=300,null=True)
    selflinks = models.CharField(max_length=300,null=True)
    updatelinks = models.CharField(max_length=300,null=True)
    yamllinks = models.CharField(max_length=300,null=True)
    tag = models.CharField(max_length=10,null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')


    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        t = []
        for x in ast.literal_eval(self.configMap):
            t.append(x)

        tmp["configMap"] = t
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_configmap'

class ProjectPvc(models.Model, ModelMixin):
    pjid = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    nsname = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    nsid = models.CharField(max_length=50, verbose_name='ranchernamespaceid唯一', null=True)
    pvcname = models.CharField(max_length=50, null=True)
    pvcid = models.CharField(max_length=50, null=True)
    storageid = models.CharField(max_length=50, null=True)
    capacity = models.CharField(max_length=30, null=True)
    accessMode= models.CharField(max_length=30, null=True)
    volumeid = models.CharField(max_length=255, null=True)
    dellinks = models.CharField(max_length=300,null=True)
    selflinks = models.CharField(max_length=300,null=True)
    updatelinks = models.CharField(max_length=300,null=True)
    yamllinks = models.CharField(max_length=300,null=True)
    tag = models.CharField(max_length=10,null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['create_by'] = self.create_by.username
        return tmp
    class Meta:
        db_table = 'rancher_pvc'


class tmp(models.Model, ModelMixin):
    STATUS_CHOOSE = (
        ('Y', 'up'),
        ('N', 'down'),
    )
    top_project = models.CharField(max_length=100,  verbose_name="所属顶级项目id",null=True)
    project_name = models.CharField(max_length=80,db_index=True, verbose_name='rancher项目名称唯一', null=True)
    project_id = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    namespace = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    namespaceid = models.CharField(max_length=50, verbose_name='rancher命名空间id唯一', null=True)
    deployname = models.CharField(max_length=80, db_index=True, verbose_name='部署服务名称(在rancher下必须唯一)', null=True)
    deployid = models.CharField(max_length=80, db_index=True, verbose_name='发布部署app唯一', null=True)
    img = models.CharField(max_length=255, verbose_name='部署镜像', null=True)
    replica = models.IntegerField(default=1, db_index=True, verbose_name='pod副本scale伸缩', null=True)
    configName = models.CharField(max_length=200, verbose_name='配置映射卷名',null=True)
    configId = models.CharField(max_length=200, verbose_name='配置映射id',null=True)
    configMap = SizedTextField(size_class=3, verbose_name='配置映射卷多[{k,v}]',null=True)
    pvcName = models.CharField(max_length=200, verbose_name='pvc配置映射卷名称',null=True)
    pvcid = models.CharField(max_length=100, verbose_name='pvcid',null=True)
    pvcSize = models.CharField(max_length=200, verbose_name='pvc配置映射卷大小',null=True)
    pvcMode = models.CharField(max_length=200, verbose_name='pvc访问模式',null=True)
    rancher_url = models.CharField(max_length=200, verbose_name="rancher前缀url", null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOOSE, default='Y', verbose_name='同步服务监控状态(关机释放下线)', null=True)
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT,default=2)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人',null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    pubsvc = models.CharField(max_length=300, verbose_name='暴露端口与服务所在部署主机地址', null=True)
    depends_svc = models.CharField(max_length=500, verbose_name="依赖服务或组件多余注释", null=True)

    class Meta:
        db_table = 'tmp'


# class ProjectServiceHistory(ProjectService, ModelMixin):
#     service = models.ForeignKey(ProjectService, on_delete=models.PROTECT, verbose_name="所属服务")
#
#     class Meta(ProjectService.Meta):
#         db_table = 'service_history'


class ProjectServiceApproval(models.Model, ModelMixin):
    STATUS_CHOOSE = (
        (-3, '发布异常'),
        (-1, '已驳回'),
        (0, '待审核'),
        (1, '待发布'),
        (2, '发布中'),
        (3, '发布成功'),
    )
    TYPES = (
        (1, '迭代发布'),
        (2, 'bug发布'),
        (3, '紧急发布'),
        (4, '回滚发布')
    )
    service = models.ForeignKey(ProjectService, on_delete=models.PROTECT, verbose_name="所属服务")
    pbtype = models.IntegerField(choices=TYPES, default='1', verbose_name="发布类型")
    opshandler = models.CharField(max_length=15,verbose_name='审核人',null=True)
    opsstatus = models.IntegerField(choices=STATUS_CHOOSE, default='0', verbose_name='ops审核状态', null=True)
    dbhandler = models.CharField(max_length=15,verbose_name='db审核人', null=True)
    dbstatus = models.IntegerField(choices=STATUS_CHOOSE, default='0', verbose_name='db审核状态', null=True)
    testhandler = models.CharField(max_length=15,verbose_name='test审核人', null=True)
    teststatus = models.IntegerField(choices=STATUS_CHOOSE, default='0', verbose_name='test审核状态', null=True)
    leaderhandler = models.CharField(max_length=15,verbose_name='leader审核人', null=True)
    leaderstatus = models.IntegerField(choices=STATUS_CHOOSE, default='0', verbose_name='leader审核状态', null=True)
    approval_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='审核时间')

    class Meta:
        db_table = 'rancher_pbapproval'

class ProjectServiceApprovalNotice(models.Model,ModelMixin):
    service = models.ForeignKey(ProjectService, on_delete=models.PROTECT, verbose_name="所属服务")
    notice_user = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="通知审核用户")
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['nickname'] = self.notice_user.nickname
        tmp['email'] = self.notice_user.email
        tmp['top_project'] = self.service.top_project
        tmp['pjname'] = self.service.pjname
        tmp['nsname'] = self.service.nsname
        tmp['dpname'] = self.service.dpname
        tmp['dpname'] = self.service.dpname

        return tmp

    class Meta:
        db_table = 'rancher_appnotice'
#
#
# class Alarm(models.Model, ModelMixin):
#     LEVEL_CHOOSE = (
#         (0, '致命'),
#         (1, '严重'),
#         (2, '一般'),
#         (3, '警告'),
#         (4, '信息'),
#     )
#     ORIGIN_CHOOSE = (
#         (0, 'zabbix'),
#         (1, 'promethues'),
#     )
#     NOTIFY_TYPE_CHOOSE = (
#         (0, 'sms;mail'),
#         (1, 'sms'),
#         (2, 'mail'),
#         (3, 'sms;mail;wechat'),
#     )
#     RECOVERY_STATUS_CHOOSE = (
#         (0, '未处理'),
#         (1, '处理中'),
#         (2, '忽略'),
#         (3, '已解决'),
#     )
#     INDICATOR_CHOOSE = (
#         (0, '网络'),
#         (1, '程序'),
#         (2, '硬件'),
#         (3, '性能'),
#         (5, '容器DCE'),
#         (6, '容器k8s'),
#         (7, '中间件'),
#         (8, 'devops'),
#         (9, '其他'),
#         (10, '安全'),
#         (11, '存储'),
#     )
#     STATUS_CHOOSE = (
#         (0, '已发送'),
#         (1, '未上报'),
#         (2, '已确认'),
#     )
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
#     recovery_time = models.DateTimeField(null=True, db_index=True, verbose_name='恢复时间')
#     ip = models.CharField(max_length=15, verbose_name='服务器ip')
#     module = models.CharField(db_index=True, max_length=128, verbose_name='业务')
#     opsper = models.CharField(max_length=64, null=True, verbose_name='运维负责人')
#     developer = models.CharField(max_length=64, null=True, verbose_name='开发负责人')
#     level = models.IntegerField(choices=LEVEL_CHOOSE, verbose_name='告警级别')
#     origin = models.IntegerField(choices=ORIGIN_CHOOSE, verbose_name='告警来源')
#     indicator = models.IntegerField(choices=INDICATOR_CHOOSE, verbose_name='告警指标')
#     notify_type = models.IntegerField(choices=NOTIFY_TYPE_CHOOSE, default=0, verbose_name='通知方式')
#     status = models.IntegerField(choices=STATUS_CHOOSE, default=1, verbose_name='发送状态')
#     recovery_status = models.IntegerField(choices=RECOVERY_STATUS_CHOOSE, default=0, verbose_name='处理状态')
#     sound_count = models.IntegerField(default=0, verbose_name='发声次数')
#     hostname = models.CharField(default='', max_length=255, verbose_name='主机名')
#     detail = models.TextField(null=True, verbose_name='告警详情')
#     device_type = models.CharField(default='其他', max_length=255, verbose_name='设备类型')
#     handler = models.CharField(max_length=100,null=True,verbose_name='处理人')
#
# class Event(models.Model,ModelMixin):
#     LEVEL_CHOOSE = (
#         (0, '普通事件'),
#         (1, '严重故障'),
#     )
#     event_name = models.CharField(null=True, max_length=255, verbose_name='事件名')
#     level = models.IntegerField(choices=LEVEL_CHOOSE, verbose_name='事件级别')
#     report = models.CharField(null=True,verbose_name="报告文件名/上传报告服务器路径")
#     handler = models.CharField(max_length=100,null=True,verbose_name='处理人')
#     create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
#
# class ServicesBackup(models.Model,ModelMixin):
#     host = models.ForeignKey(CMDB,on_delete=models.PROTECT, verbose_name="所属主机备份脚本")
#     name = models.CharField(max_length=128,verbose_name="脚本名")
#     content = models.TextField(verbose_name="脚本内容")
#     crontime = models.CharField(max_length=128, verbose_name="定时周期")
#     backupstatus = models.CharField(max_length=128, verbose_name="状态")
#     comment = models.CharField(max_length=255, null=True)
#     create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
#
# class CheckReport(models.Model,ModelMixin):
#     CHECK_CHOOSE = (
#         (0,'未审核'),
#         (1, '已审核')
#     )
#     system = models.CharField(max_length=128,verbose_name="巡检系统")
#     system_url = models.CharField(max_length=128,verbose_name="巡检系统连接")
#     screen = models.CharField(max_length=255,verbose_name="巡检截图/文件名")
#     sys_check = models.CharField(choices=CHECK_CHOOSE,verbose_name="审核")
#     create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
#
# class BrowserTag(models.Model,ModelMixin):
#     name = models.CharField(max_length=128,verbose_name="标签名")
#     url = models.TextField(verbose_name="标签地址")
#     create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
#     create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
#     modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')


class RancherProject(models.Model, ModelMixin):
    # top_project = models.ForeignKey(CMDB, on_delete=models.PROTECT, verbose_name="所属顶级项目", )
    project_name = models.CharField(db_index=True, max_length=80, verbose_name='rancher项目名称')
    project_id = models.CharField(max_length=50, verbose_name='rancher项目id')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')

    class Meta:
        db_table = 'rancher_project'
        unique_together = ("env", "project_name", "project_id")


class RancherNamespace(models.Model, ModelMixin):
    project = models.ForeignKey(RancherProject, on_delete=models.PROTECT, verbose_name="所属项目")
    namespace = models.CharField(max_length=50, verbose_name='命名空间')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')

    class Meta:
        db_table = 'rancher_namespace'
        unique_together = ("env", "namespace", "project")


class RancherDeployment(models.Model, ModelMixin):
    project = models.ForeignKey(RancherProject, on_delete=models.PROTECT, verbose_name="所属项目")
    namespace = models.ForeignKey(RancherNamespace, on_delete=models.PROTECT, verbose_name='所属命名空间')
    deployname = models.CharField(max_length=80, db_index=True, verbose_name='部署appname')
    img = models.CharField(max_length=255, verbose_name='部署img')
    pubsvc = models.CharField(max_length=300, default="0", verbose_name='暴露端口与服务地址')
    deployid = models.CharField(max_length=80, db_index=True, verbose_name='部署app唯一')
    deploy_type = models.CharField(max_length=80, default="0", db_index=True, verbose_name='部署类型')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    createts = models.BigIntegerField(verbose_name="创建时间戳用来计算差异过去的时间回滚")
    state = models.CharField(max_length=80, db_index=True, verbose_name='状态')
    replica = models.IntegerField(default=1, db_index=True, verbose_name='副本scale伸缩')
    volumes_detail = SizedTextField(size_class=3, verbose_name='配置映射卷list')
    volumes = models.CharField(max_length=100, db_index=True, verbose_name='关联数据卷')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['namespace'] = self.namespace.namespace
        tmp['envname'] = self.env.name
        tmp['project'] = self.project.project_name
        tmp['project_id'] = self.project.project_id
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_deployment'
        unique_together = ("env", "deployname", "deployid", "namespace", "project")


class RancherPublishHistory(models.Model, ModelMixin):
    service = models.ForeignKey(ProjectService,null=True, on_delete=models.PROTECT, verbose_name="所属服务")
    top_project = models.CharField(max_length=200, verbose_name="所属顶级项目")
    toppjid = models.CharField(max_length=200, verbose_name="所属顶级项目id")
    pjname = models.CharField(db_index=True, max_length=80, verbose_name='rancher项目名称唯一', null=True)
    pjid = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    nsname = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    nsid = models.CharField(max_length=50, verbose_name='ranchernamespaceid唯一', null=True)
    dpname = models.CharField(max_length=80, db_index=True, verbose_name='部署服务名称(在rancher下必须唯一)', null=True)
    dpid = models.CharField(max_length=80, db_index=True, verbose_name='发布部署app唯一', null=True)
    img = models.CharField(max_length=255, verbose_name='部署镜像', null=True)
    replica = models.IntegerField(default=1, db_index=True, verbose_name='pod副本scale伸缩', null=True)
    configId = models.CharField(max_length=200, verbose_name='configId')
    configName = models.CharField(max_length=200, verbose_name='配置映射卷名')
    configMap = SizedTextField(size_class=3, verbose_name='配置映射卷多[{k,v}]', default='[]')
    rancher_url = models.CharField(max_length=200, verbose_name="rancher前缀url", null=True)
    state = models.CharField(max_length=50, default='Y', verbose_name='同步服务监控状态(关机释放下线)', null=True)
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人',null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    pubsvc = models.CharField(max_length=300, verbose_name='暴露端口与服务所在部署主机地址', null=True)
    v_mount = models.CharField(max_length=1500,verbose_name="挂载详情",null=True)
    volumes = models.CharField(max_length=1500,verbose_name="卷详情",null=True)
    cbox_env = models.CharField(max_length=1500,verbose_name="容器变量",null=True)
    verifyurl = models.CharField(max_length=255,verbose_name='rancher app check',null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        return tmp

    class Meta:
        db_table = 'rancher_pbhistory'

class RancherSvcPubStandby(models.Model, ModelMixin):
    PUB_TYPE = (
       (1,'迭代发布'),
       (2,'bug发布'),
       (3,'紧急发布'),
    )
    DP_TYPE = (
       (1,'rancher'),
       (2,'host'),
    )
    app = models.ForeignKey(App, on_delete=models.PROTECT,null=True)
    service = models.ForeignKey(ProjectService,null=True, on_delete=models.PROTECT, verbose_name="所属服务")
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间',null=True)
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间',null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人',null=True)
    deploy_type = models.IntegerField(choices=DP_TYPE,default=1, null=True, verbose_name='部署类型 host / rancher')
    pbtype = models.IntegerField(choices=PUB_TYPE, default=1, verbose_name='publish类型',null=True)
    top_project = models.CharField(max_length=200, verbose_name="所属顶级项目",null=True)
    toppjid = models.CharField(max_length=200, verbose_name="所属顶级项目id",null=True)
    pjname = models.CharField(db_index=True, max_length=80, verbose_name='rancher项目名称唯一', null=True)
    pjid = models.CharField(max_length=50, verbose_name='rancher项目id唯一', null=True)
    nsname = models.CharField(max_length=50, verbose_name='rancher命名空间名称唯一', null=True)
    nsid = models.CharField(max_length=50, verbose_name='ranchernamespaceid唯一', null=True)
    dpid = models.CharField(max_length=80, db_index=True, verbose_name='部署app唯一',null=True)
    dpname = models.CharField(max_length=80, db_index=True, verbose_name='部署appname',null=True)
    v_mount = models.CharField(max_length=1500,verbose_name="挂载详情",null=True)
    volumes = models.CharField(max_length=1500,verbose_name="卷详情",null=True)
    cbox_env = models.CharField(max_length=1500,verbose_name="容器变量",null=True)
    verifyurl = models.CharField(max_length=255,verbose_name='rancher app check',null=True)
    configId = models.CharField(max_length=200, verbose_name='configId',null=True)
    configName = models.CharField(max_length=200, verbose_name='配置映射卷名',null=True)
    configMap = SizedTextField(size_class=3, verbose_name='配置映射卷多[{k,v}]', default='[]',null=True)
    rancher_url = models.CharField(max_length=200, verbose_name="rancher前缀url", null=True)
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人',null=True)
    pubsvc = models.CharField(max_length=300, verbose_name='暴露端口与服务所在部署主机地址', null=True)
    img = models.CharField(max_length=255, verbose_name='部署img',null=True)
    update_img = models.BooleanField(verbose_name="更新镜像",null=True)
    is_audit = models.BooleanField(verbose_name="是否审核",null=True)
    replica = models.IntegerField(default=1, db_index=True, verbose_name='副本scale伸缩',null=True)
    state = models.BooleanField(verbose_name="发布状态", null=True)
    publish_time = models.DateTimeField(null=True,verbose_name="定时发布时间 未来")

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        return tmp

    class Meta:
        db_table = 'rancher_publish'


class RancherConfigMap(models.Model, ModelMixin):
    project = models.ForeignKey(RancherProject, on_delete=models.PROTECT, verbose_name="所属项目")
    namespace = models.ForeignKey(RancherNamespace, on_delete=models.PROTECT, verbose_name='所属命名空间')
    configname = models.CharField(max_length=100, db_index=True, verbose_name='配置文件名')
    configid = models.CharField(max_length=100, verbose_name='配置文件更新id')
    configMap_k = models.CharField(max_length=100, db_index=True, verbose_name='配置映射键')
    configMap_v = SizedTextField(size_class=3, verbose_name='配置映射内容')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')
    old_id = models.IntegerField(default=0)

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['namespace'] = self.namespace.namespace
        tmp['envname'] = self.env.name
        tmp['project'] = self.project.project_name
        tmp['project_id'] = self.project.project_id
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_configmapbak'
        unique_together = ("env", "configname", "namespace")


class RancherConfigMapVersion(models.Model, ModelMixin):
    project = models.ForeignKey(RancherProject, on_delete=models.PROTECT, verbose_name="所属项目")
    namespace = models.CharField(max_length=100)
    configname = models.CharField(max_length=100, db_index=True, verbose_name='配置文件名')
    configid = models.CharField(max_length=100, verbose_name='配置文件更新id')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    configMap_k = models.CharField(max_length=100, db_index=True, verbose_name='配置映射键')
    configMap_v = SizedTextField(size_class=3, verbose_name='配置映射内容')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    old_id = models.IntegerField()
    env_id = models.IntegerField()

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['project'] = self.project.project_name
        tmp['project_id'] = self.project.project_id
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_configmaphisotry'
        # unique_together = ("id", "configid")
        ordering = ('-create_time',)
