from django.db import models
from apps.account.models import User
from libs import ModelMixin
# Create your models here.
class EmailRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    from_email = models.CharField(max_length=64, verbose_name='发件人邮箱')
    to_email = models.CharField(max_length=64, verbose_name='收件人邮箱')
    subject = models.CharField(default='', max_length=1000, verbose_name='邮件主题')
    content = models.TextField(verbose_name='邮件内容')
    is_pushed = models.BooleanField(default=False, verbose_name='是否已经发送')

    def __iter__(self):
        return self

    class Meta:
        db_table = 'email'
        app_label = 'message'
        verbose_name = '邮件记录'
        verbose_name_plural = '邮件记录'


class LoggerTaskRecord(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    action_task = models.CharField(max_length=64, db_index=True,verbose_name='task')
    content = models.TextField(verbose_name='邮件内容')
    status = models.IntegerField(verbose_name='执行状态')


    class Meta:
        db_table = 'task_record'
        app_label = 'message'

class LoggerOpRecord(models.Model,ModelMixin):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, verbose_name='创建人')
    content = models.TextField(verbose_name='操作内容')
    action = models.CharField(max_length=20, db_index=True,verbose_name='op')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['opuser'] = self.create_by.nickname
        return tmp

    class Meta:
        db_table = 'spug_record'
        app_label = 'message'
        ordering = ('-id',)
