from django.contrib.auth.models import AbstractUser
from django.db import models

"""
1.django的用户类可以集成django提供的类
"""


class User(AbstractUser):
    """"用户模型类"""
    # 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        # 定义创建的表名
        db_table = 'tb_users'

        # 后台的显示
        verbose_name = '用户'
        verbose_name_plural = verbose_name
