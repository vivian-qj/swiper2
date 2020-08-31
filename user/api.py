import os
from lib.http import render_json
from user.logic import send_verity_code, check_vcode,save_upload_file
from user.models import User
from common import error
from user.forms import ProfileForm,UploadForm
from swiper import settings

# Create your views here.

def get_verity_code(request):
    '''手机注册'''
    phonenum = request.GET.get('phonenum')
    send_verity_code(phonenum)
    return render_json(None)

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
        return render_json(user.to_dict())
    else:
        # return render_json(None,1000) 1000表示错误码，也需要我们定义
        return render_json(None, error.VCODE_ERROR())

def get_profile(request):
    user = request.user
    return render_json(user.profile.to_dict())

def modify_profile(request):
    '''修改个人资料'''
    '''
    form = ProfileForm(request.POST)
    if form.is_valid():
        user = request.user
        user.profile.__dict__.update(form.cleaned_data)
        user.profile.save()

        return render_json(None)
    '''
    form1 = ProfileForm(request.POST)
    if form1.is_valid():
        form1.save()
        return render_json(None)
    else:
        return render_json(error.PROFILE_ERROR)

def upload_avatar(request):
    '''头像上传'''
    #1.接受用户上传的头像
    #2.定义用户头像名称
    #3.异步将头像上传七牛云
    #4.将URL保存入数据库
    '''
     print('11111111111111111111111111111111')

    print(request.POST)
    print(request.FILES)
    for name , file in request.FILES.items():
        print(name , file )#k是文件名。v是文件本身
        ext_name = os.path.splitext(name)[-1]
        print(ext_name)
        filename = 'Avatar-%s%s' % (request.session['uid'], ext_name)#最好跟用户关联,头像重命名
        from pickle import dumps
        print(dumps(file))

    return render_json(None)
    '''



    file =request.FILES.get('avatar')
    if file:
        save_upload_file(request.user, file)
        return render_json(None)
    else:
        render_json(None, error.FILE_NOT_FOUND)

