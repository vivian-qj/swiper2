from lib.http import render_json
from user.logic import send_verity_code, check_vcode
from user.models import User
from common import error
# Create your views here.

def get_verity_code(request):
    '''手机注册'''
    phonenum = request.GET.get('phonenum')
    send_verity_code(phonenum)
    return render_json(None, 0)

def login(request):
    '''短信验证登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        #获取用户
        user, created = User.objects.get_or_create(phonenum=phonenum)

        #记录登录用户状态
        request.session['uid'] = user.id
        # return render_json(user,0) json 渲染user对象，在models中修改建立字典
        return render_json(user.to_dict(), 0)
    else:
        # return render_json(None,1000) 1000表示错误码，也需要我们定义
        return render_json(None, error.VCODE_ERROR())

def get_profile(request):
    pass

