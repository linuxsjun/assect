from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests, json, time, datetime, hashlib, random


from base.models import configs
from hr.models import employee, user_sign_log

# Create your views here.

def index(request):
    context = {}
    username = request.COOKIES.get('usercookie', None)
    if username:
        try:
            signuser = employee.objects.get(session=username)
        except Exception:
            context['userinfo'] = '用户'
            return render(request, 'sign.html', context)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    return render(request, 'base.html', context)


def config(request):
    context={}
    context['title']='设置'

    username = request.COOKIES.get('usercookie', None)
    if username:
        try:
            signuser = employee.objects.get(session=username)
        except Exception:
            context['userinfo'] = '用户'
            return render(request, 'sign.html', context)
        context['userinfo'] = signuser.name
    else:
        context['userinfo'] = '用户'
        return render(request, 'sign.html', context)

    try:
        ps = configs.objects.get(pk = 1)
    except AttributeError:
        print('AttributeError')
        return render(request, 'base_conf.html', context)
    except configs.DoesNotExist:
        # context['corpid'] = 'ww74c5af840cdd5cb6'
        # context['corpsecret'] = 'uUJf-eFplyKlAWf2Cc9T8Guea4K1zpEiZXwXpCsHTQs'
        return render(request, 'base_conf.html', context)

    context['context'] = ps
    return render(request, 'base_conf.html', context)


def create_corpid(request):
    if request.method == "POST":
        if request.POST["corpid"]:
            corpidstr = request.POST['corpid']
    try:
        ps = configs.objects.get(pk=1)
    except configs.DoesNotExist:
        newpk = configs(corpid=corpidstr)
        newpk.save()
    else:
        ps.corpid = corpidstr
        ps.save()
    return HttpResponse(corpidstr)


def sign_view(request):
    context={}
    context['userinfo'] = '登录'
    context['stat'] = 'CLItMYby44wD8vgM'
    request.encoding = 'utf-8'
    if request.method == "POST":
        if request.POST["user"]:
            seluser = request.POST['user']
            empusers =employee.objects.all()
            # print(empusers)
            if empusers:
                users = employee.objects.filter(userid=seluser)
                if users:
                    u = users.first()
                    rnd = seluser + str(time.time()) + str(random.randint(10000, 20000))
                    strsession = hashlib.md5()
                    strsession.update(rnd.encode('utf-8'))
                    s = strsession.hexdigest()
                    u.session = s
                    u.save()

                    #登录日志
                    # wlog = user_sign_log.objects.create(signtime=datetime.datetime.fromtimestamp(time.time()),
                    #                           employeeid=u,
                    #                           fromip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                    #                           contl='user&passwd')
                    # wlog.save()

                    gourl = redirect('/')
                    gourl.set_cookie('usercookie', s, 14400)

                    return gourl
            else:
                # 添加初始数据
                fuser = employee(
                    userid='admin',
                    name='Admin',
                )
                fuser.save()

    elif request.method == "GET":
        if 'code' in request.GET:
            if request.GET['code']:
                code = request.GET['code']

                url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
                v = {}
                v['corpid'] = 'ww74c5af840cdd5cb6'
                v['corpsecret'] = 'HBzQYMHZHw1UwQcqDI8GBsTnTTRJA_ODkgZuo2QuT28'

                r = requests.get(url, params=v)
                t = json.loads(r.text)

                url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo'
                v = {}
                v['access_token'] = t['access_token']
                v['code'] = code

                r = requests.get(url, params=v)
                t = json.loads(r.text)

                seluser = t['UserId']
                users = employee.objects.filter(userid=seluser)
                if users:
                    u = users.first()
                    rnd = seluser + str(time.time()) + str(random.randint(10000, 20000))
                    strsession = hashlib.md5()
                    strsession.update(rnd.encode('utf-8'))
                    s = strsession.hexdigest()
                    u.session = s
                    u.save()

                    # 登录日志
                    wlog = user_sign_log(signtime=datetime.datetime.fromtimestamp(time.time()),
                                              employeeid=u,
                                              fromip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
                                              contl='Scan WX-code')
                    wlog.save()

                    gourl = redirect('/')
                    gourl.set_cookie('usercookie', s, 14400)
                    return gourl
        else:
            print('code is no')

    return render(request, 'sign.html', context)


def signout(request):
    username = request.COOKIES.get('usercookie', None)
    try:
        signuser = employee.objects.get(session=username)
        signuser.session = '0000000000000000'
        # signuser.expsession = 0
        signuser.save()

        gourl = redirect('/')
        gourl.delete_cookie('username')
        return gourl
    except Exception:
        return redirect('/')
    return redirect('/')