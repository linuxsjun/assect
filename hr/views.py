from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg, Sum, Max, Min, Count

import requests
import json
import datetime

from base.models import configs, wxsecret
from hr.models import hrconfigs, employee, department, employee_department
from attendance.models import checkinout

from . import wxdef

# Create your views here.
def index(request):
    return redirect('/hr/hr/')


def hr_list(request):
    context = {}
    context['title'] = '人员'

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

    # d = base_conf.objects.all().first()
    # ps = hr_department.objects.all().order_by('parentid','order')
    # ps = hr_department.objects.filter(parentid=1).order_by('pid', 'order')
    ps = employee.objects.filter(active=True).values().order_by('name')
    context['context'] = ps
    return render(request, 'hr_employee_list.html', context)


def hr_detailed(request):
    context = {}
    context['title'] = '人员'

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

    if request.method == "GET":
        print(request.GET)
        if "id" in request.GET:
            empid = int(request.GET['id'])

            ps = employee.objects.filter(pk=empid).values('name',
                                                          'position',
                                                          'extemployeeatt__pin',
                                                          'userid').first()

            # ==============================
            # count_data = storage_log.objects.filter(CreateTime__year=this_year, CreateTime__month=this_month)\
            #     .extra(select={"CreateTime": "DATE_FORMAT(CreateTime,'%%e')"})\
            #     .values('CreateTime')\
            #     .annotate(send_num=Count('CreateTime'))\
            #     .values('CreateTime', 'count_len')

            e = ps['extemployeeatt__pin']
            print(e)
            attch = checkinout.objects.filter(pin=e, checktime__year=2016, checktime__month=9)\
                .values('pin', 'checktime')\
                .order_by('checktime')

            # attch = checkinout.objects.filter(pin=e).values_list('checktime')
            print(attch)
            print(len(attch))
            # ================================

            emps = employee_department.objects.filter(employeeid=ps['userid']).values('id', 'departmentid__name')
            ps['emps'] = emps

            department_isleaders = employee_department.objects.filter(isleader=True, employeeid=ps['userid']).values('id',
                                                                                                                     'departmentid__name')
            ps['dep_isleaders'] = department_isleaders
            context['context'] = ps

            print("======")
            print(ps)
            return render(request, 'hr_employee_detailed.html', context)

    elif request.method == "POST":
        if "act" in request.POST:
            if request.POST['act'] == "create":
                pass


def dep_list(request):
    context={}
    context['title'] = '部门'

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

    if request.method == "GET":
        ps = department.objects.filter(type=0)\
            .values('id', 'pid', 'name', 'parentid')\
            .order_by('pid')
        context['context'] = ps

        deps = []
        for k in ps:
            # 查找负责人
            leaders = employee_department.objects.filter(isleader=True, departmentid=k['pid'])\
                .values('id', 'employeeid__name')
            if leaders is None:
                pass
            else:
                k['leaders'] = leaders

            # 查找部门员工
            employeecount = employee_department.objects.filter(departmentid=k['pid'])\
                .values('departmentid_id')\
                .annotate(employeesum=Count('id'))
            # print(k['name'])
            # print(employeecount)
            if employeecount:
                k['employeenum'] = employeecount[0]['employeesum']
            else:
                k['employeenum'] = 0

            # 查找子部门
            departmentcount = department.objects.filter(parentid=k['pid'])\
                .values('parentid')\
                .annotate(departmentsum=Count('id'))
            # print(k['name'])
            # print(departmentcount)
            if departmentcount:
                k['departmentsum'] = departmentcount[0]['departmentsum']
            else:
                k['departmentsum'] = 0

            deps.append(k)
        context['context'] = deps

        parents = department.objects.all().order_by('name')
        context['parents'] = parents

        employees= employee.objects.filter(active=True).order_by('name')
        context['employees'] = employees
        return render(request, 'hr_department_list.html', context)

    elif request.method == "POST":
        print(request.POST)
        data = {}
        if "act" in request.POST:
            if request.POST['act'] == "create":
                # 查找可用Pid
                pidmax = department.objects.all().values('pid').order_by('pid').last()
                pida = pidmax['pid'] + 1
                # 查找上一级
                parentinp = int(request.POST['parent'])
                if parentinp:
                    mparentobj = department.objects.get(id=parentinp)
                    mparentid = mparentobj.pid
                else:
                    mparentid = 0
                # 查找平级，取order值
                ordermax = department.objects.filter(parentid=parentinp)\
                    .values()\
                    .order_by('-order')\
                    .first()
                if ordermax is None:
                    ordera = 100000000
                else:
                    ordera = ordermax['order'] + 1
                # 新建到数据库
                nitem = department(pid=pida,
                                   name=request.POST['name'],
                                   parentid=mparentid,
                                   order=ordera,
                                   type=0)
                nitem.save()
                # 查找负责人
                leaderinp = int(request.POST['leader'])
                if leaderinp:
                    leaderid = employee.objects.get(id=leaderinp)

                # 是否要同步
                syncwx = wxsecret.objects.filter(agentid=1)
                if syncwx:
                    # 同步到企业微信
                    print(pida)
                    nwxdep = department.objects.filter(pid=pida).values()
                    print(nwxdep)
                    wxmsg=wxdef.depcreate(nwxdep.first())
                    data = json.dumps(wxmsg)
                    return HttpResponse(data, content_type="application/json")
            elif request.POST['act'] == "update":
                print('update')
            elif request.POST['act'] == "delete":
                dpid = int(request.POST['pid'])
                # 确认是否还有子内容，如有返回报错
                findsubs = department.objects.filter(parentid=dpid)
                print(findsubs)
                if findsubs:
                    data['code'] = 402
                    data['msg'] = 'Fail'
                    data['data'] = "部门下含有子部门，删除失败。"
                    data = json.dumps(data)
                    return HttpResponse(data, content_type="application/json")
                else:
                    findemps = employee_department.objects.filter(departmentid=dpid)
                    if findemps:
                        data['code'] = 403
                        data['msg'] = 'Fail'
                        data['data'] = "部门下含有员工，删除失败。"
                        data = json.dumps(data)
                        return HttpResponse(data, content_type="application/json")
                    else:
                        # 没有子内容，可以删除
                        ps = department.objects.filter(pid=dpid)
                        ps.delete()
                        data['code'] = 0
                        data['msg'] = "OK"
                        data['data'] = None
                        data = json.dumps(data)

                        #  删除同步到企业微信
                        # 是否要同步
                        syncwx = wxsecret.objects.filter(agentid=1)
                        if syncwx.exists():
                            # 同步到企业微信
                            wxmsg = wxdef.depdelete(dpid)
                            data = json.dumps(wxmsg)
                        return HttpResponse(data, content_type="application/json")
        return render(request, 'hr_department_list.html', context)


def confbase_view(request):
    context={}
    context['title']='常规设置'

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

    context['context']= ''
    return render(request, 'hr_conf_base.html', context)


def confmore_view(request):
    context={}
    context['title'] = '高级设置'

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

    context['context'] = ''
    return render(request, 'hr_conf_more.html', context)


def wx_corpsecret_save(request):
    print(request.POST)
    if request.method == "POST":
        if request.POST["corpsecret"]:
            corpsecretstr = request.POST['corpsecret']
    try:
        ps = wxsecret.objects.get(agentid=1)
    except wxsecret.DoesNotExist:
        newitem = wxsecret(name="通讯录", agentid=1, corpsecret=corpsecretstr)
        newitem.save()
    else:
        ps.corpsecret = corpsecretstr
        ps.save()
    return HttpResponse('kkk')


def wx_syncfromwx(request):
    data = {}
    tokenstr = wxdef.getdepartment()
    tokenstr = wxdef.gethr()

    data['code'] = 0
    data['msg'] = 'OK'
    data['data'] = "同步员工信息成功"
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")
