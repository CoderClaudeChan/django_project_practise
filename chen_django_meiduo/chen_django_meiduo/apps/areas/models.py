from django.db import models


class Areas(models.Model):
    """行政区划模型类"""
    name = models.CharField(max_length=20, verbose_name='名称')

    # subs查询所有下属行政区划
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



