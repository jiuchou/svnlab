from django.db import models
# from datetime import date
from django.utils import timezone

# Create your models here.
class Report(models.Model):
    STATE_CHOICES = ( (0, '进行中'), (1, '安装中'), (2, '失败') )
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
        managed = True
        db_table = 'report'
