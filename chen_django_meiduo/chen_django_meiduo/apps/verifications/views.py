import random

from django_redis import get_redis_connection
from redis.client import Pipeline
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import constants


class SMScodeView(APIView):
    """发送短信验证码业务"""
    # url('^sms_code/(?P<mobile>1[3-9]\d{9})/$')
    # 1.获取手机号

    # 2.获取验证码，并保存在redis

    # 3.发送短信验证码,60s内不能重复发送(通过存一个标记在redis1里面提取验证)

    # 4.发送成功
    def get(self, request, mobile):
        # 创建redis连接，需要指定是哪个redis
        redis_conn = get_redis_connection('verify_code')

        # 获取60s发送标记
        sms_flag = redis_conn.get('sms_flag_%s' % mobile)
        if sms_flag:
            return Response({'message': '发送过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 发送验证码
        print(sms_code)

        # 保存验证码
        # 创建管道可以避免redis经常开闭降低性能
        # 创建管道对象
        pl = redis_conn.pipeline()  # type: Pipeline
        # 保存验证码，有效时间60s
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 保存60s的标记
        pl.setex('sms_flag_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, 1)

        # 执行
        pl.execute()

        # 发送成功
        return Response({'message': 'OK'})