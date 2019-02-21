import os

from celery import Celery


# 为celery使用django配置文件进行配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chen_django_meiduo.settings.dev')

# 创建celery应用
celery_app = Celery('meiduo')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.email'])
