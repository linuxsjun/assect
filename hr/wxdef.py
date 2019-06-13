import requests, json, time, datetime

from base.models import configs, wxsecret
from hr.models import employee, extattr, department, employee_department

def getToken(agentidnum):
    d = configs.objects.get(pk=1)
    corpidstr = d.corpid

    appsecret = wxsecret.objects.get(agentid=agentidnum)
    corpsecretstr = appsecret.corpsecret

    gnow = datetime.datetime.now()
    exttime = appsecret.expirestime

    if (exttime is None) or (exttime < gnow):
        #https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRECT
        # corpid=ww74c5af840cdd5cb6
        # corpsecret=uUJf-eFplyKlAWf2Cc9T8Guea4K1zpEiZXwXpCsHTQs

        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        v = {}
        v['corpid'] = corpidstr
        v['corpsecret'] = corpsecretstr

        r = requests.get(url, params=v)
        t = json.loads(r.text)

        if t['errcode'] == 0:
            appsecret.token = t['access_token']

            tt = time.time()
            appsecret.expirestime = datetime.datetime.fromtimestamp(tt + t['expires_in'])

            appsecret.save()
            response = appsecret.token
        else:
            response = "None"
    else:
        response = appsecret.token

    return(response)

def gethr(department_id = 1,fetch_child = 1):
    # https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID&fetch_child=FETCH_CHILD
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/list'
    # https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID&fetch_child=FETCH_CHILD
    # url = 'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist'

    agentidnum = 1

    v = {}
    v['access_token'] = getToken(agentidnum)
    v['department_id'] = department_id
    v['fetch_child'] = fetch_child

    r = requests.get(url, params=v)
    t = json.loads(r.text)
    # print(t)

    if t['errcode'] == 0:
        d = {}
        for d in t['userlist']:
            # print(d)
            try:
                chkem=None
                chkem = employee.objects.filter(userid=d['userid'])

            except Exception:
                print('chkem error')
                pass

            if chkem:
                # Todo 略过
                #记录已存在
                l = employee.objects.get(userid=d['userid'])

                l.userid = d['userid']
                u_name = d['name']
                l.position = d['position']
                l.mobile = d['mobile']
                u_gender = d['gender']
                l.email = d['email']
                l.avatar = d['avatar']
                u_status = d['status']
                u_enable = d['enable']
                u_isleader = d['isleader']
                u_extattr = d['extattr']
                u_hide_mobile = d['hide_mobile']
                u_english_name = d['english_name']
                l.telephone = d['telephone']
                u_order = d['order']
                if 'external_profile' in d:
                    l.external_profile = str(d['external_profile'])
                    # print(u_name)
                    # print(d['external_profile'])
                else:
                    l.external_profile = None
                u_qr_code = d['qr_code']
                u_alias = d['alias']
                if 'address' in d:
                    l.address = d['address']
                else:
                    l.address = None
                l.save()
            else:
                u_userid = d['userid']
                u_name = d['name']
                u_position = d['position']
                u_mobile = d['mobile']
                u_gender = d['gender']
                u_email = d['email']
                u_avatar = d['avatar']
                u_status = d['status']
                u_enable = d['enable']
                u_isleader = d['isleader']
                u_extattr = d['extattr']
                u_hide_mobile = d['hide_mobile']
                u_english_name = d['english_name']
                u_telephone = d['telephone']
                u_order = d['order']
                if 'external_profile' in d:
                    u_external_profile = str(d['external_profile'])
                    # print(u_name)
                    # print(d['external_profile'])
                else:
                    u_external_profile = None
                u_qr_code = d['qr_code']
                u_alias = d['alias']
                if 'address' in d:
                    u_address = d['address']
                else:
                    u_address = None

                dt = employee(userid=u_userid,
                           name=u_name,
                           position=u_position,
                           mobile=u_mobile,
                           gender=u_gender,
                           email=u_email,
                           avatar=u_avatar,
                           status=u_status,
                           enable=u_enable,
                           isleader=u_isleader,
                           extattr=u_extattr,
                           hide_mobile=u_hide_mobile,
                           english_name=u_english_name,
                           telephone=u_telephone,
                           order=u_order,
                           external_profile=u_external_profile,
                              qr_code=u_qr_code,
                              alias=u_alias,
                              address=u_address,
                              wxsync=True)
                try:
                    dt.save()
                except:
                    print('no')
                    pass
                # print(u_name)
                #
                # print(d['department'])
                # print(d['is_leader_in_dept'])

            nemp = employee.objects.get(userid=d['userid'])
            # 关联员工与
            if 'external_profile' in d:
                if 'external_attr' in d['external_profile']:
                    for i in d['external_profile']['external_attr']:
                        if i['type'] == 0:
                            cc = extattr.objects.get_or_create(empid=nemp,
                                                               type=i['type'],
                                                               name=i['name'],
                                                               value=i['text']['value'])
                        elif i['type'] == 1:
                            cc = extattr.objects.get_or_create(empid=nemp,
                                                               type=i['type'],
                                                               name = i['name'],
                                                               url=i['web']['url'],
                                                               title=i['web']['title'])
                        elif i['type'] == 2:
                            print(2)
                        pass
                if 'external_corp_name' in d['external_profile']:
                    print('---------', d['external_profile']['external_corp_name'])

            # 关联员工与部门
            ii = 0
            for dd in d['department']:
                try:
                    dep = department.objects.filter(pid=int(dd)).first()
                except Exception:
                    pass
                else:
                    try:
                        rep = employee_department.objects.filter(employeeid=nemp.userid, departmentid=dep)
                    except Exception:
                        pass
                    else:
                        if len(rep):
                            pass
                        else:
                            kk = list(d['is_leader_in_dept'])
                            seds = employee_department(employeeid=nemp, departmentid=dep, isleader=kk[ii])
                            try:
                                seds.save()
                            except:
                                pass

                ii += 1
    return(0)

def getdepartment(depid = 1):
    # https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=ACCESS_TOKEN&id=ID
    agentidnum = 1

    url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list'
    v = {}
    v['access_token'] = getToken(agentidnum)
    v['id'] = depid

    try:
        r = requests.get(url, params=v)
    except Exception:
        print('get url is error')
    else:
        t = json.loads(r.text)
        if t['errcode'] == 0:
            d = {}
            for d in t['department']:
                dt = department(pid=d['id'],
                                   name=d['name'],
                                   parentid=d['parentid'],
                                   order=d['order'])
                try:
                    dt.save()
                except:
                    pass
    return(0)

def depcreate(newdep):
    # 使用编辑前,要修改"企业微信"中"通讯录同步"的权限为"编辑"权限,目前为"只读"权限
    agentidnum = 1

    context = {}
    context['access_token'] = getToken(agentidnum)
    val={}
    val['name'] = newdep['name']
    val['parentid'] = newdep['parentid']
    val['order'] = newdep['order']
    val['id'] = newdep['pid']

    urls = 'https://qyapi.weixin.qq.com/cgi-bin/department/create'
    data = {}
    try:
        x = requests.post(urls, params=context, json=val)
    except Exception:
        data['code'] = 404
        data['msg'] = 'Fail'
        data['data'] = 'get url is error'
    else:
        t = json.loads(x.text)
        print(t)
        # {'errcode': 48002, 'errmsg': 'api forbidden, hint: [1554653557_4_0d1eac6bc6f0b5860ec3449603c38813], more info at https://open.work.weixin.qq.com/devtool/query?e=48002'}
        if t['errcode'] == 0:
            data['code'] = 0
            data['msg'] = 'OK'
            data['data'] = None
        elif t['errcode'] == 48002:
            print('22222')
            data['code'] = 404
            data['msg'] = 'Fail'
            data['data'] = '修改"企业微信"中"通讯录同步"的权限为"编辑"权限(48002)'
        else:
            data['code'] = 400
            data['msg'] = 'Fail'
            data['data'] = t['errmsg']
    return(data)

def depupdate():
    # Todo 更新到数据库,并生成不重复PID

    # 同步到企业微信
    p = configs.objects.all().first()

    context = {}
    context['access_token'] = p.token
    val = {
        "parentid": 25,
        "id": 2
    }

    urls = 'https://qyapi.weixin.qq.com/cgi-bin/department/update'
    x = requests.post(urls, params=context, json=val)
    print(x.url)
    print(x.content)

    return

def depdelete(depid):
    # 删除更新到数据库
    agentidnum = 1
    context = {}
    context['access_token'] = getToken(agentidnum)
    context['id'] = depid

    urls = 'https://qyapi.weixin.qq.com/cgi-bin/department/delete'
    data = {}
    try:
        x = requests.get(urls, params=context)
    except Exception:
        data['code'] = 404
        data['msg'] = 'Fail'
        data['data'] = 'get url is error'
    else:
        t = json.loads(x.text)
        print(t)
        if t['errcode'] == 0:
            data['code'] = 0
            data['msg'] = 'OK'
            data['data'] = None
        elif t['errcode'] == 48002:
            data['code'] = 404
            data['msg'] = 'Fail'
            data['data'] = '修改"企业微信"中"通讯录同步"的权限为"编辑"权限(48002)'
        elif t['errcode'] == 60123:
            data['code'] = 404
            data['msg'] = 'Fail'
            data['data'] = '无效的部门ID(60123)'
        else:
            data['code'] = 400
            data['msg'] = 'Fail'
            data['data'] = t['errmsg']
    return(data)
