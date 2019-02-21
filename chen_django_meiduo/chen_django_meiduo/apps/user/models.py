from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import BadData
from itsdangerous.jws import TimedJSONWebSignatureSerializer

import constants

"""
1.django的用户类可以集成django提供的类
"""


class User(AbstractUser):
    """"用户模型类"""
    # 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

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



