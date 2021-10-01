# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin, human_datetime
from apps.account.models import User
from apps.setting.utils import AppSetting
from libs.ssh import SSH
from apps.config.models import  Environment

class Host(models.Model, ModelMixin):
    STATUS_CHOOSE = (
        ('Y', 'up'),
        ('N', 'down'),
    )
    top_project = models.CharField(max_length=128, verbose_name="顶级项目", null=True)
    top_projectid = models.CharField(max_length=100, verbose_name="顶级项目id", null=True)
    ipaddress = models.CharField(max_length=15, verbose_name="ip", null=True)
    service_pack = models.CharField(max_length=500, verbose_name="包含哪些服务类型包'',''", null=True)
    osType = models.CharField(max_length=155,verbose_name='系统类型', null=True)
    osVerion = models.CharField(max_length=100,verbose_name='发行版本', null=True)
    coreVerion = models.CharField(max_length=100,verbose_name='内核版本', null=True)
    # disks_format = models.CharField(max_length=255,verbose_name='数据盘格式', null=True)
    disk = models.TextField(verbose_name="disk arguments",null=True)
    disks = models.IntegerField(verbose_name='数据盘数量', null=True)
    # disks_capacity = models.CharField(max_length=255, verbose_name="数据盘容量'',''", null=True)
    memory = models.IntegerField(verbose_name='内存GB', null=True)
    cpus = models.IntegerField(default=0, verbose_name='cpu数量', null=True)
    cpucore = models.IntegerField(default=0, verbose_name='cpu物理核', null=True)
    serial_num = models.CharField(verbose_name='序列号', max_length=100, null=True)
    status = models.CharField(max_length=15,choices=STATUS_CHOOSE, default='Y', verbose_name='同步监控状态(关机释放下线)', null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', null=True)
    supplier = models.CharField(max_length=100, verbose_name='供应商', null=True)
    host_bug = models.CharField(max_length=500, verbose_name='服务版本与是否打补丁['','']', null=True)
    ext_config1 = models.CharField(max_length=255, verbose_name='扩展信息', null=True)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人' ,null=True)
    zone = models.CharField(max_length=50,verbose_name="分组", null=True)
    # create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    # name = models.CharField(max_length=50)
    # hostname = models.CharField(max_length=50)
    port = models.IntegerField(null=True)
    username = models.CharField(max_length=50,null=True)
    pkey = models.TextField(null=True)
    desc = models.CharField(max_length=255, null=True)

    created_at = models.CharField(max_length=20, default=human_datetime)
    # created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    # deleted_at = models.CharField(max_length=20, null=True)
    # deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    @property
    def private_key(self):
        return self.pkey or AppSetting.get('private_key')

    def get_ssh(self, pkey=None):
        pkey = pkey or self.private_key
        ### hostname - >  ipaddress
        return SSH(self.ipaddress, self.port, self.username, pkey)
    #
    # def __repr__(self):
    #     return '<Host %r>' % self.name
    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['create_by'] = self.create_by.username
        return tmp

    class Meta:
        db_table = 'hosts'
        ordering = ('-id',)
