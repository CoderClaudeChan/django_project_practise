import constants
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import BadData
from itsdangerous.jws import TimedJSONWebSignatureSerializer
from chen_django_meiduo.utils.models import BaseModel

"""
1.django的用户类可以集成django提供的类
"""


class User(AbstractUser):
    """"用户模型类"""
    # 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    # 添加默认地址
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        # 定义创建的表名
        db_table = 'tb_users'

        # 后台的显示
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):
        """生成验证邮箱链接（加密后的）"""
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)

        data = {'user_id': self.id, 'email': self.email}

        token = serializer.dumps(data).decode()  # type: str

        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token

        return verify_url

    @staticmethod
    def check_verify_email_token(token):
        """检查验证邮件的token"""
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)

        try:
            data = serializer.loads(token)

        except BadData:
            return None
        else:
            email = data.get('email')
            user_id = data.get('user_id')

            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user


class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省份')
    city = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='city_addresses',
                             verbose_name='市区')
    district = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']





