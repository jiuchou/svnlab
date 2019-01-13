"""
user.models
~~~~~~~~~

This module implements the Requests Models.

:copyright: (c) 2019 by JiuChou.
:license: MIT, see LICENSE for more details.
:updateTime: 2019.01.13
"""

from django.db import models
from django.utils import timezone

# Create your models here.
class UserInfo(models.Model):
    """
        state: {
            token: getToken(),
            avatar: "",
            userInfo: {
                username: "guster",
                truename: "",
                sex: "male",
                email: "xxx@dahuatech.com",
                introduction: "",
                avatar: ""
            }
        }
    """
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    truename = models.CharField(max_length=64)
    sex = models.CharField(verbose_name="sex", max_length=5, choices=(("male", "male"), ("female", "female")), default="male")
    email = models.EmailField()
    telephone = models.CharField(max_length=64, unique=True)
    introduction = models.CharField(max_length=512)
    profile_photos_height = models.PositiveIntegerField(default=75)
    profile_photos_width = models.PositiveIntegerField(default=75)
    profile_photos = models.ImageField(upload_to="profile_photos", height_field="profile_photos_height", width_field="profile_photos_width")
    join_time = models.DateTimeField("加入时间", default=timezone.now)
    login_time = models.DateTimeField("最后登录时间", auto_now=True)

    # [1] https://segmentfault.com/q/1010000006121303
    # python2: def __unicode__
    def __str__(self):
        return self.username

    class Meta:
        """docstring
        """
        managed = True
        db_table = "user_info"
        # 一个字符串的列表或元组, 每个字符串是一个字段名
        #   前面带有可选的"-"前缀表示倒序
        #   前面没有"-"的字段表示正序
        #   使用"?"来表示随机排序
        ordering = ["-username"]

class Role(models.Model):
    """docstring
    """
    username = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=300, blank=True, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    path = models.CharField(max_length=300, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)
    manager = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        """docstring
        """
        managed = True
        db_table = "user_role"
