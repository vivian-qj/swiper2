#常规配置可以去celery官方文档查询  搜config
broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000 # broker 连接池，默认10

timezone = 'Asia/Shanghai'
# using serializer name
accept_content = ['pickle','json']

task_serializer = 'pickle'


result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_cache_max = 10000  # 任务结果最大缓存数量
result_expires = 3600 # 任务过期时间

worker_redirect_stdouts_level = 'INFO' #日志
