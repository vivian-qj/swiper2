'''
第三方配置
'''

#互亿无线短信配置
HY_SMS_URL = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
HY_SMS_PARAMS = {
    'account': 'C33173714',
    'password': '45bf499027e3e0d217f2de6bde70a0b6',
    'content': '您的验证码是：%s。请不要把验证码泄露给其他人。',
    'mobile': None,
    'format': 'json'
}

#七牛云配置
QN_ACCESS_KEY = '2DitSFNog1ueMoVMmKZKqLKUoz1By8qZNdwZS3V4'
QN_SECRET_KEY =  'M6JqbRbOOZpQj_TmBN1dJ1-41rer4sd-1ErSoulG'
QN_BUCKET_NAME = 'vivia' #创建的空间名
QN_BASE_URL = 'http://qexzoeyxn.hd-bkt.clouddn.com'
