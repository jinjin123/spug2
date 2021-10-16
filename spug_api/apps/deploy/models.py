# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs import ModelMixin, human_datetime
from apps.account.models import User
from apps.app.models import Deploy


class DeployRequest(models.Model, ModelMixin):
    STATUS = (
        ('-3', '发布异常'),
        ('-1', '已驳回'),
        ('0', '待审核'),
        ('1', '待发布'),
        ('2', '发布中'),
        ('3', '发布成功'),
    )
    TYPES = (
        ('1', '迭代发布'),
        ('2', 'bug发布'),
        ('3', '紧急发布'),
        ('4', '回滚'),
    )
    STATUS_CHOOSE = (
        (-3, '发布异常'),
        (-1, '已驳回'),
        (0, '待审核'),
        (1, '待发布'),
        (2, '发布中'),
        (3, '发布成功'),
    )

    deploy = models.ForeignKey(Deploy, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=TYPES, default='1')
    extra = models.TextField()
    host_ids = models.TextField()
    desc = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=2, choices=STATUS)
    reason = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=50, null=True)

    created_at = models.CharField(max_length=20, default=human_datetime)
    created_by = models.ForeignKey(User, models.PROTECT, related_name='+')
    approve_at = models.CharField(max_length=20, null=True)
    approve_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)
    do_at = models.CharField(max_length=20, null=True)
    do_by = models.ForeignKey(User, models.PROTECT, related_name='+', null=True)

    # pbtype = models.IntegerField(choices=TYPES, default='1', verbose_name="发布类型")
    opshandler = models.CharField(max_length=15,verbose_name='审核人',null=True)
    opsstatus = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='ops审核状态', null=True)
    dbhandler = models.CharField(max_length=15,verbose_name='db审核人', null=True)
    dbstatus = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='db审核状态', null=True)
    testhandler = models.CharField(max_length=15,verbose_name='test审核人', null=True)
    teststatus = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='test审核状态', null=True)
    leaderhandler = models.CharField(max_length=15,verbose_name='leader审核人', null=True)
    leaderstatus = models.IntegerField(choices=STATUS_CHOOSE, default=0, verbose_name='leader审核状态', null=True)
    approval_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='审核时间')

    def __repr__(self):
        return f'<DeployRequest name={self.name}>'

    class Meta:
        db_table = 'deploy_requests'
        ordering = ('-id',)
