# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin, human_datetime
from apps.account.models import User
from apps.setting.utils import AppSetting
from libs.ssh import SSH
from apps.config.models import  Environment
import ast
# from django.contrib.auth.hashers import make_password, check_password
from libs.pwd import encryptPwd,decryptPwd

class Host(models.Model, ModelMixin):
    STATUS_CHOOSE = (
        (0, '在线'),
        (1, '离线'),
    )
    PV_CHOOSE = (
        (0, '电信'),
        (1, '联通'),
        (2, '移动'),
    )
    PT_CHOOSE = (
        (0, '主机'),
        (1, '数据库'),
        (2, 'redis'),
    )
    OS_TYPE = (
        (0, 'Linux'),
        (1, 'Windows'),
    )
    # TOP_PJCHOOSE  = {
    #     (0, '东莞市政务数据大脑暨智慧城市IOC运行中心建设项目'),
    #     (1, '东莞市疫情动态查询系统项目'),
    #     (2, '东莞市疫情防控数据管理平台项目'),
    #     (3, '东莞市跨境货车司机信息管理系统项目'),
    #     (4, '疫情地图项目'),
    #     (5, '粤康码'),
    # }
    top_project = models.CharField(max_length=180, verbose_name="顶级项目", null=True)
    child_project = models.CharField(max_length=180, verbose_name="子项目", null=True)
    # top_projectid = models.CharField(max_length=100, verbose_name="顶级项目id", null=True)
    ipaddress = models.CharField(max_length=255, verbose_name="ip", null=True)
    service_pack = models.CharField(max_length=500, verbose_name="包含哪些服务类型包'',''", null=True)
    osType = models.CharField(max_length=155,verbose_name='系统类型', null=True)
    osVerion = models.CharField(max_length=100,verbose_name='发行版本', null=True)
    coreVerion = models.CharField(max_length=100,verbose_name='内核版本', null=True)
    # disks_format = models.CharField(max_length=255,verbose_name='数据盘格式', null=True)
    disk = models.TextField(verbose_name="disk arguments",null=True)
    disks = models.IntegerField(verbose_name='数据盘数量', null=True)
    # disks_capacity = models.CharField(max_length=255, verbose_name="数据盘容量'',''", null=True)
    # memory = models.FloatField(verbose_name='内存GB', null=True)
    memory = models.IntegerField(verbose_name='内存GB', null=True)
    cpus = models.IntegerField(default=0, verbose_name='cpu逻辑数量', null=True)
    # cpucore = models.IntegerField(default=0, verbose_name='cpu物理核', null=True)
    # serial_num = models.CharField(verbose_name='序列号', max_length=100, null=True)
    status = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='同步监控状态(关机释放下线)', null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', null=True)

    cluster = models.CharField(max_length=100,verbose_name="cluster",null=True)
    # ostp = models.IntegerField(choices=OS_TYPE,verbose_name="os type",null=True)
    ostp = models.CharField(max_length=100,verbose_name="os type",null=True)
    # provider = models.IntegerField(choices=PV_CHOOSE,verbose_name='运营商', null=True)
    provider = models.IntegerField(verbose_name='运营商', null=True)
    # resource_type = models.IntegerField(choices=PT_CHOOSE,verbose_name="资产类型",null=True)
    resource_type = models.CharField(max_length=50,verbose_name="资产类型",null=True)
    work_zone = models.CharField(max_length=20,verbose_name="work area",null=True)
    outter_ip = models.CharField(max_length=255, verbose_name="outerip", null=True)
    v_ip = models.CharField(max_length=255, verbose_name="v_ip", null=True)
    use_for =models.CharField(max_length=255,verbose_name="use for" ,null=True)
    password_hash = models.BinaryField(null=True,verbose_name="pwd")
    password_date = models.DateTimeField(auto_now=True,null=True,verbose_name="create")
    password_expire = models.IntegerField(null=True,verbose_name="expire ")
    sys_disk = models.CharField(max_length=255,verbose_name="sys disk", null=True)
    data_disk = models.TextField(verbose_name="data_disk", null=True)
    sys_data = models.CharField(max_length=500,verbose_name="sys+data", null=True)
    dbrelation = models.IntegerField(verbose_name='master/slave/cluster/none',null=True,default=4)
    dbtag = models.CharField(max_length=100,verbose_name="IP_V",null=True)

    supplier = models.CharField(max_length=100, verbose_name='供应商', null=True)
    # host_bug = models.CharField(max_length=500, verbose_name='服务版本与是否打补丁['','']', null=True)
    # ext_config1 = models.CharField(max_length=255, verbose_name='扩展信息', null=True)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人' ,null=True)
    zone = models.CharField(max_length=255,verbose_name="资源类别", null=True)
    # create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    # name = models.CharField(max_length=50)
    # hostname = models.CharField(max_length=50)
    port = models.IntegerField(null=True)
    username = models.CharField(max_length=50,null=True)
    pkey = models.TextField(null=True)
    shili = models.CharField(max_length=500, null=True)
    comment = models.CharField(max_length=255, null=True)
    iprelease = models.CharField(max_length=255, verbose_name="待回收ip", null=True)
    created_at = models.CharField(max_length=20, default=human_datetime)
    # created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    deleted_at = models.CharField(max_length=20, null=True)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    @staticmethod
    def make_password(plain_password: str) -> str:
        # return make_password(plain_password, hasher='pbkdf2_sha256')
        return encryptPwd(plain_password)

    # @staticmethod
    # def plaxt_password(crytto):
    #     return decryptPwd(crytto)

    # def verify_password(self, plain_password: str) -> bool:
    #     return check_password(plain_password, self.password_hash)
    @staticmethod
    def conver_disk(disk):
        tt = ""
        if disk != "[]"  and  disk != "" and disk is not None and not isinstance(disk,list):
            for x in ast.literal_eval(disk):
                tt += "数据盘:"+x.get("name")+";容量:"+str(x.get("size"))+"G;"
            return tt
        else:
            return ""

    @staticmethod
    def tosys_disk(disk):
        tt = ""
        if disk != "[]"  and  disk != "" and disk is not None and not isinstance(disk,list):
            for x in ast.literal_eval(disk):
                tt = "系统盘:" + x.get("name") + ";容量:" + str(x.get("total_size")) + "G;"
            return tt
        else:
            return ""

    @staticmethod
    def convert_str_list(data):
        tt = []
        if data != "[]" and data != "" and data is not None and not isinstance(data,list):
            tt = ast.literal_eval(data)
            return tt
        else:
            return tt

    @property
    def private_key(self):
        return self.pkey or AppSetting.get('private_key')

    def get_ssh(self, pkey=None):
        pkey = pkey or self.private_key
        ### hostname - >  ipaddress
        return SSH(self.ipaddress, self.port, (ConnctUser.objects.get(pk=self.username)).name, pkey)
    #
    # def __repr__(self):
    #     return '<Host %r>' % self.name
    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        # tt = ""
        # for x in ast.literal_eval(self.disk):
        #     tt += "类型:"+x.get("type")+",数据盘:"+x.get("name")+",挂载目录:"+x.get("mount")+",总大小:"+str(x.get("total_szie"))+"G,数据盘已使用"+str(x.get("used"))+"G,"
        # tmp["disk"] = self.conver_disk(self.data_disk)
        tmp["sys_disk"] = self.tosys_disk(self.sys_disk)
        tmp["data_disk"] = self.conver_disk(self.data_disk)
        tmp['create_by'] = self.create_by.nickname
        # tmp['env'] = "生产" if self.env_id == 2 else "测试"
        tmp['status'] =  "在线" if self.status == 0 else "离线"
        tmp["zone"] = self.convert_str_list(self.zone)
        tmp["username"] = self.convert_str_list(self.username)
        tmp["resource_type"] = self.convert_str_list(self.resource_type)
        tmp["cluster"] = self.convert_str_list(self.cluster)
        tmp["service_pack"] = self.convert_str_list(self.service_pack)
        tmp["work_zone"] = self.convert_str_list(self.work_zone)
        tmp["top_project"] = self.convert_str_list(self.top_project)
        tmp["child_project"] = self.convert_str_list(self.child_project)
        # tmp["ostp"] = "Linux" if self.ostp == 0 else "Windows"
        # tmp['provider'] = self.get_provider_display()
        # tmp['resource_type'] = self.get_resource_type_display()
        # tmp['top_project'] = self.get_top_project_display()
        # tmp['password_hash'] = self.plaxt_password(bytes(self.password_hash,encoding='utf-8'))
        tmp['password_hash'] = decryptPwd(self.password_hash) if self.password_hash else ""
        return tmp

    class Meta:
        db_table = 'hosts'
        ordering = ('-id',)

class MultiDBUser(models.Model, ModelMixin):
    STATUS_CHOOSE = (
        (0, '在线'),
        (1, '离线'),
    )
    PV_CHOOSE = (
        (0, '电信'),
        (1, '联通'),
        (2, '移动'),
    )
    PT_CHOOSE = (
        (0, '主机'),
        (1, '数据库'),
        (2, 'redis'),
    )
    OS_TYPE = (
        (0, 'Linux'),
        (1, 'Windows'),
    )

    top_project = models.CharField(max_length=180, verbose_name="顶级项目", null=True)
    child_project = models.CharField(max_length=180, verbose_name="子项目", null=True)
    # top_projectid = models.CharField(max_length=100, verbose_name="顶级项目id", null=True)
    ipaddress = models.CharField(max_length=255, verbose_name="ip", null=True)
    service_pack = models.CharField(max_length=500, verbose_name="包含哪些服务类型包'',''", null=True)
    osType = models.CharField(max_length=155,verbose_name='系统类型', null=True)
    osVerion = models.CharField(max_length=100,verbose_name='发行版本', null=True)
    coreVerion = models.CharField(max_length=100,verbose_name='内核版本', null=True)
    # disks_format = models.CharField(max_length=255,verbose_name='数据盘格式', null=True)
    disk = models.TextField(verbose_name="disk arguments",null=True)
    disks = models.IntegerField(verbose_name='数据盘数量', null=True)
    # disks_capacity = models.CharField(max_length=255, verbose_name="数据盘容量'',''", null=True)
    # memory = models.FloatField(verbose_name='内存GB', null=True)
    memory = models.IntegerField(verbose_name='内存GB', null=True)
    cpus = models.IntegerField(default=0, verbose_name='cpu逻辑数量', null=True)
    # cpucore = models.IntegerField(default=0, verbose_name='cpu物理核', null=True)
    # serial_num = models.CharField(verbose_name='序列号', max_length=100, null=True)
    status = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='同步监控状态(关机释放下线)', null=True)
    hostname = models.CharField(max_length=100, verbose_name='主机名', null=True)

    cluster = models.CharField(max_length=100,verbose_name="cluster",null=True)
    # ostp = models.IntegerField(choices=OS_TYPE,verbose_name="os type",null=True)
    ostp = models.CharField(max_length=100,verbose_name="os type",null=True)
    # provider = models.IntegerField(choices=PV_CHOOSE,verbose_name='运营商', null=True)
    provider = models.IntegerField(verbose_name='运营商', null=True)
    # resource_type = models.IntegerField(choices=PT_CHOOSE,verbose_name="资产类型",null=True)
    resource_type = models.CharField(max_length=50,verbose_name="资产类型",null=True)
    work_zone = models.CharField(max_length=20,verbose_name="work area",null=True)
    outter_ip = models.CharField(max_length=255, verbose_name="outerip", null=True)
    v_ip = models.CharField(max_length=255, verbose_name="v_ip", null=True)
    use_for =models.CharField(max_length=255,verbose_name="use for" ,null=True)
    password_hash = models.BinaryField(null=True,verbose_name="pwd")
    password_date = models.DateTimeField(auto_now=True,null=True,verbose_name="create")
    password_expire = models.IntegerField(null=True,verbose_name="expire ")
    sys_disk = models.CharField(max_length=255,verbose_name="sys disk", null=True)
    data_disk = models.TextField(verbose_name="data_disk", null=True)
    sys_data = models.CharField(max_length=500,verbose_name="sys+data", null=True)


    supplier = models.CharField(max_length=100, verbose_name='供应商', null=True)
    # host_bug = models.CharField(max_length=500, verbose_name='服务版本与是否打补丁['','']', null=True)
    # ext_config1 = models.CharField(max_length=255, verbose_name='扩展信息', null=True)
    developer = models.CharField(max_length=200, verbose_name='开发负责人',null=True)
    opsper = models.CharField(max_length=200, verbose_name='运维负责人' ,null=True)
    zone = models.CharField(max_length=255,verbose_name="资源类别", null=True)
    # create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    env = models.ForeignKey(Environment, verbose_name='环境', null=True,on_delete=models.PROTECT)
    # name = models.CharField(max_length=50)
    # hostname = models.CharField(max_length=50)
    port = models.IntegerField(null=True)
    username = models.CharField(max_length=50,null=True)
    pkey = models.TextField(null=True)
    shili = models.CharField(max_length=500, null=True)
    comment = models.CharField(max_length=255, null=True)
    iprelease = models.CharField(max_length=500, verbose_name="待回收ip", null=True)
    created_at = models.CharField(max_length=20, default=human_datetime)
    # created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    deleted_at = models.CharField(max_length=20, null=True)
    deleted_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    @staticmethod
    def make_password(plain_password: str) -> str:
        # return make_password(plain_password, hasher='pbkdf2_sha256')
        return encryptPwd(plain_password)

    @staticmethod
    def conver_disk(disk):
        tt = ""
        if disk != "[]"  and  disk != "" and disk is not None and not isinstance(disk,list):
            for x in ast.literal_eval(disk):
                tt += "数据盘:"+x.get("name")+";容量:"+str(x.get("size"))+"G;"
            return tt
        else:
            return ""

    @staticmethod
    def tosys_disk(disk):
        tt = ""
        if disk != "[]"  and  disk != "" and disk is not None and not isinstance(disk,list):
            for x in ast.literal_eval(disk):
                tt = "系统盘:" + x.get("name") + ";容量:" + str(x.get("total_size")) + "G;"
            return tt
        else:
            return ""

    @staticmethod
    def convert_str_list(data):
        tt = []
        if data != "[]" and data != "" and data is not None and not isinstance(data,list):
            tt = ast.literal_eval(data)
            return tt
        else:
            return tt

    @property
    def private_key(self):
        return self.pkey or AppSetting.get('private_key')

    def get_ssh(self, pkey=None):
        pkey = pkey or self.private_key
        ### hostname - >  ipaddress
        return SSH(self.ipaddress, self.port, (ConnctUser.objects.get(pk=self.username)).name, pkey)
    #
    # def __repr__(self):
    #     return '<Host %r>' % self.name
    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        # tt = ""
        # for x in ast.literal_eval(self.disk):
        #     tt += "类型:"+x.get("type")+",数据盘:"+x.get("name")+",挂载目录:"+x.get("mount")+",总大小:"+str(x.get("total_szie"))+"G,数据盘已使用"+str(x.get("used"))+"G,"
        # tmp["disk"] = self.conver_disk(self.data_disk)
        tmp["sys_disk"] = self.tosys_disk(self.sys_disk)
        tmp["data_disk"] = self.conver_disk(self.data_disk)
        tmp['create_by'] = self.create_by.nickname
        # tmp['env'] = "生产" if self.env_id == 2 else "测试"
        tmp['status'] =  "在线" if self.status == 0 else "离线"
        tmp["zone"] = self.convert_str_list(self.zone)
        tmp["username"] = self.convert_str_list(self.username)
        tmp["resource_type"] = self.convert_str_list(self.resource_type)
        tmp["cluster"] = self.convert_str_list(self.cluster)
        tmp["service_pack"] = self.convert_str_list(self.service_pack)
        tmp["work_zone"] = self.convert_str_list(self.work_zone)
        tmp["top_project"] = self.convert_str_list(self.top_project)
        tmp["child_project"] = self.convert_str_list(self.child_project)
        # tmp["ostp"] = "Linux" if self.ostp == 0 else "Windows"
        # tmp['provider'] = self.get_provider_display()
        # tmp['resource_type'] = self.get_resource_type_display()
        # tmp['top_project'] = self.get_top_project_display()
        # tmp['password_hash'] = self.plaxt_password(bytes(self.password_hash,encoding='utf-8'))
        tmp['password_hash'] = decryptPwd(self.password_hash) if self.password_hash else ""
        return tmp

    class Meta:
        db_table = 'multidb'
        ordering = ('-id',)

class Datadisk(models.Model, ModelMixin):
    disk = models.TextField(null=True,verbose_name="disk")
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
         db_table = "host_disk"


class ClusterConfig(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
         db_table = "cluster_config"


class WorkZone(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "work_zone"

class Zone(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "zone"


class Servicebag(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "servicebag"

class Portlist(models.Model,ModelMixin):
    # name = models.CharField(max_length=50)
    ipaddress = models.CharField(max_length=15)
    port = models.CharField(max_length=255)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "portlist"


class DevicePositon(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "device_position"

class ConnctUser(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "connect_user"
        ordering = ('name',)

class ResourceType(models.Model,ModelMixin):
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "resource_type"

class Domainlist(models.Model,ModelMixin):
    domain = models.CharField(max_length=50)
    ipaddress = models.CharField(max_length=255)
    comment = models.CharField(max_length=500, null=True)
    created_by = models.ForeignKey(User, models.PROTECT, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间')

    class Meta:
        db_table = "domain_list"


class SystemCheck(models.Model,ModelMixin):
    STATUS_CHOOSE = (
        (0, '正常'),
        (1, '不正常'),
    )
    name = models.CharField(max_length=255,db_index=True,null=True)
    url = models.CharField(max_length=500,null=True)
    check_time = models.DateField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    status = models.IntegerField(choices=STATUS_CHOOSE, null=True,db_index=True)

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        # tmp['status'] = self.get_status_display()
        return tmp

    class Meta:
        db_table = "system_check"
        ordering = ('-check_time',)


class SystemHealthInfo(models.Model,ModelMixin):
    STATUS_CHOOSE = (
        (0, '安全容量'),
        (1, '危险容量'),
        (2, '警戒容量'),
    )
    ipaddress = models.CharField(max_length=255, verbose_name="ip", null=True)
    cpublance = models.CharField(max_length=100, verbose_name="bl", null=True)
    cpus = models.IntegerField(default=0, verbose_name='cpu逻辑数量', null=True)
    meminfo = models.CharField(max_length=255, verbose_name="mem", null=True)
    memblance = models.CharField(max_length=255, verbose_name="membl", null=True)
    diskinfo = models.CharField(max_length=3000, verbose_name="disk", null=True)
    diskstatus = models.IntegerField(choices=STATUS_CHOOSE, null=True,db_index=True)
    check_time = models.DateField(auto_now_add=True, db_index=True, verbose_name='创建时间')
    status = models.IntegerField(choices=STATUS_CHOOSE, null=True,db_index=True)


    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        return tmp


    class Meta:
        db_table = "system_hard"
        ordering = ('-status','-diskstatus')



