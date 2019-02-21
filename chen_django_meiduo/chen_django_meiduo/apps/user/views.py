from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user import serializers
from user.models import User


class UsernameCountView(APIView):
    """判断用户名是否存在"""
    # url(r'^usernames/(?P<username>\w{5, 20})/count/$')

    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count,
        }

        return Response(data)


class MobileCountView(APIView):
    """判断手机号是否存在"""
    # url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$')
    def get(self, request, mobile):

        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count,
        }

        return Response(data=data)


class UserView(CreateAPIView):
    """注册功能"""
    # url(r'^ursers/$')
    # 创建序列化器实现
    serializer_class = serializers.CreateUserSerialiser


class UserDetailView(RetrieveAPIView):
    """用户详情数据接口"""
    # url(r'^user/')
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        return self.request.user


class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    """
    # url(r'^email/^')
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyEmailView(APIView):
    """邮箱验证"""
    # url(r'^email/verification/$ ')
    def get(self, request):
        #　获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})










