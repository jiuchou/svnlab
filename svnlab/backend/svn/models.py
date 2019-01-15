"""
svn.models
~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.14
"""

from django.db import models
from django.utils import timezone

class SvnList(models.Model):
    """svn信息检索
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    dir_n = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    number = models.CharField(max_length=40, blank=True, null=True)
    base_url = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        """SvnList meta data.
        """
        managed = True
        db_table = 'svn_list'
        app_label = 'svninfo'

# Create your models here.
class Report(models.Model):
    """定义svn操作记录
    包含
        影响人
        申请人
        旧权限
        新权限
        操作状态
        申请来源
        申请时间
        最后更新时间
    """
    STATE_CHOICES = ((0, '进行中'), (1, '安装中'), (2, '失败'))
    identifier = models.CharField(max_length=64, unique=True)
    path = models.CharField(max_length=512)
    username = models.CharField(max_length=64)
    applicant = models.CharField(max_length=64)
    old_role = models.CharField(max_length=64)
    new_role = models.CharField(max_length=643)
    state = models.IntegerField(choices=STATE_CHOICES)
    apply_source = models.CharField(max_length=64)
    # apply_time = models.DateField(default=date.today)
    # update_time = models.DateField(default=date.today)
    apply_time = models.DateTimeField('申请时间', default=timezone.now)
    update_time = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        """Roport meta data.
        """
        managed = True
        db_table = 'svn_report'
