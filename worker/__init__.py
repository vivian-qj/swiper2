import os
from celery import Celery
from celery import platforms

#设置环境变量，加载django的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','swiper.settings')

#创建Celery Application
celery_app = Celery('swiper')
celery_app.config_from_object('worker.config') # 加载模块的配置
celery_app.autodiscover_tasks() # 自动加载通过装饰器定义的所有的任务

platforms.C_FORCE_ROOT = True

def call_by_worker(func):
    '''将任务在celery中异步执行'''
    task = celery_app.task(func)  #这是一个装饰器

    return task.delay
#每次需要调用的是task.delay太过于累赘,将task重新装饰，以后直接调用func这个函数，返回的是task.delay