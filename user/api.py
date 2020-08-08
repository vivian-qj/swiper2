from lib.http import render_json
from user.logic import send_verity_code
# Create your views here.

def get_verity_code(request):
    '''手机注册'''
    phonenum = request.POST.get('phonenum')
    send_verity_code(phonenum)
    return render_json(None, 0)

def login(request):
    '''短信验证登录'''
    pass

