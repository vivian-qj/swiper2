import random
import requests
import os
from urllib.parse import urljoin
from django.core.cache import cache
from swiper import config,settings
from worker import call_by_worker
from lib.qncloud import async_upload_to_qiniu


def gen_verity_code(length=6):
    '''产生一个验证码'''
    return random.randrange(10**(length-1),10**length)

@call_by_worker
def send_verity_code(phonenum):
    vcode = gen_verity_code()
    key = 'VerityCode-%s' % phonenum
    cache.set(key, vcode ,120)

    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['content'] = sms_cfg['content'] % vcode
    sms_cfg['mobile'] = phonenum
    response = requests.post(config.HY_SMS_URL, data=sms_cfg)
    return response


def check_vcode(phonenum, vcode):
    '''检查验证码是否正确'''
    key = 'VerityCode-%s' % phonenum
    saved_vcode = cache.get(key)
    return saved_vcode == vcode

def save_upload_file(user, upload_file):
    '''保存文件并上传到七牛云'''
    #获取文件并保存到本地
    ext_name = os.path.splitext(upload_file.name)[-1]
    filename = 'Avatar-%s%s' % (user.id, ext_name)  # 最好跟用户关联,头像重命名
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)

    with open(filepath, 'wb') as newfile:
        for chunk in upload_file.chunks():  # 当文件很大时，直接保存会占据很大内存，硬盘会卡死一段时间，最好一块块写，chunk是一个生成器的形式
            newfile.write(chunk)

    #异步将头像上传到七牛
    async_upload_to_qiniu(filepath,filename)#异步上传到七牛

    #将url保存入数据库
    url = urljoin(config.QN_BASE_URL, filename)
    user.avatar = url
    user.save()


def upload_avatar_to_qiniu():
    '''异步上传到七牛'''