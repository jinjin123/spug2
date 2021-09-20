# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin, human_datetime
from apps.account.models import User
from apps.config.models import Environment
import json
from django_mysql.models.fields import SizedTextField


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


class RancherProject(models.Model, ModelMixin):
    project_name = models.CharField(db_index=True, max_length=80, verbose_name='项目名称')
    project_id = models.CharField(max_length=50, verbose_name='项目id')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')

    class Meta:
        db_table = 'rancher_project'
        unique_together = ("env", "project_name","project_id")


class RancherNamespace(models.Model, ModelMixin):
    project = models.ForeignKey(RancherProject, on_delete=models.PROTECT, verbose_name="所属项目")
    namespace = models.CharField(max_length=50, verbose_name='命名空间')
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, on_delete=models.PROTECT, default=1, verbose_name='环境')

    class Meta:
        db_table = 'rancher_namespace'
        unique_together = ("env", "namespace","project")


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
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_configmap'
        unique_together = ("env", "configname","namespace")


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
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'rancher_configmaphisotry'
        # unique_together = ("id", "configid")
        ordering = ('-create_time',)
