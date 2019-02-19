import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler


# 1.获取文件配置的定义的logger对象
logger = logging.getLogger('django')


def my_exception_handler(exc, context):
    """
    自定义异常
    :param exc: 异常
    :param context: 抛出异常上下文
    :return: Response 对象
    """
    # 调用DRF的异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        # 处理未被捕捉的DRF异常，保存到日志

        view = context['view']

        error = '[%s] %s' % (view, exc)

        logger.error(error)

        response = Response({'message': '服务器内部异常: %s' % error}, 500)

    return response

