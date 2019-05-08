from django.shortcuts import render, HttpResponse
from django.db.models import Max, Min, Count

from attendance.models import checkinout, extemployeeatt
from hr.models import employee

import datetime
import time
import threading
from xml.etree.ElementTree import parse

# Create your views here.

def index(request):
    context={}
    context['title'] = '签到'



    daystart = datetime.datetime.strptime('2019-5-7', '%Y-%m-%d')
    daytoday = datetime.datetime.strptime('2019-4-27', '%Y-%m-%d')

    ps = checkinout.objects.filter(checktime__year=daystart.year,
                                   checktime__month=daystart.month,
                                   checktime__day=daystart.day).values().order_by('-checktime')
    emppins = employee.objects.exclude(extemployeeatt__pin=None).order_by('employee_department__departmentid__name', 'name').values('name', 'extemployeeatt__pin', 'employee_department__departmentid__name')
    pinsdict = {}
    for i in emppins:
        pinsdict[i['extemployeeatt__pin']] = i
        del pinsdict[i['extemployeeatt__pin']]['extemployeeatt__pin']
    p = []
    for k in ps:
        if k['pin']:
            if k['pin'] in pinsdict:
                k.update(pinsdict[k['pin']])
        p.append(k)
    context['context'] = p




    p = []
    emppins = employee.objects.exclude(extemployeeatt__pin=None).order_by('employee_department__departmentid__name', 'name').values('name', 'extemployeeatt__pin', 'employee_department__departmentid__name')
    for emppin in emppins:
        body = emppin['extemployeeatt__pin']
        ps = checkinout.objects.filter(checktime__year=daystart.year,
                                       checktime__month=daystart.month,
                                       checktime__day=daystart.day,
                                       pin=body)\
            .values('pin')\
            .annotate(last=Max('checktime'), fast=Min('checktime'), count=Count('userid'))
        # e = checkinout.objects.filter(checktime__year=daystart.year,
        #                                checktime__month=daystart.month,
        #                                checktime__day=daystart.day,
        #                                pin=body) \
        #     .values().order_by('checktime')
        # print(e)
        if ps:
            j = dict(emppin, **ps[0])
            j['long'] = j['last'] - j['fast']
            p.append(j)
        context['context2'] = p


    return render(request, 'att_attendance_list.html', context)


def summary(request):
    context={}
    context['title'] = '出勤'
    return render(request, 'att_summary_list.html', context)


def att_collect_detail(request):
    context={}
    context['title'] = '明细'
    return render(request, 'att_collect_detailed.html', context)


def attclass(request):
    context={}
    context['title'] = '班次'
    return render(request, 'att_class_board.html', context)


def configatt(request):
    return HttpResponse('configatt')


def institem(items=None):
    for userid, checktime, checktype, verifycode, sensorid, memoinfo, workcode, sn, userextfmt, logid, id in items:
        nitem = checkinout.objects.get_or_create(userid=userid,
                                                 checktime=checktime,
                                                 checktype=checktype,
                                                 verifycode=verifycode,
                                                 sensorid=sensorid,
                                                 memoinfo=memoinfo,
                                                 workcode=workcode,
                                                 sn=sn,
                                                 userextfmt=userextfmt)


def inputxml(request):
    with open('CHECKINOUT.XML', 'r', encoding="UTF-8") as f:
        et = parse(f)
    root = et.getroot()
    checkinouts = []
    for childone in root:
        item = []
        for childtwo in childone:
            item.append(childtwo.text)
            # print(childtwo.tag, ":", childtwo.text)
        checkinouts.append(item)
        # print(item)

    i = 0
    threads = []
    itemgroup = []
    for item in checkinouts:
        item.append(i)
        itemgroup.append(item)
        if (i % 2000) == 0:
            thread = threading.Thread(target=institem, args=(tuple(itemgroup),))
            threads.append(thread)
            itemgroup = []
        i += 1
    if itemgroup:
        thread = threading.Thread(target=institem, args=(tuple(itemgroup),))
        threads.append(thread)

    for threadrun in threads:
        threadrun.start()
    while True:
        if len(threading.enumerate()) <= 3:
            print('='*24)
            break
        time.sleep(5)
        print(len(threading.enumerate()))
    print('all done')

    with open('USERINFO.xml', 'r', encoding="UTF-8") as f:
        et = parse(f)
    root = et.getroot()
    checkinouts = []
    for childone in root:
        item = []
        for childtwo in childone:
            item.append(childtwo.text)
        checkinouts.append(item)
    for useritem in checkinouts:
        checkinouts = checkinout.objects.filter(userid=useritem[0])
        if checkinouts:
            checkinouts.update(pin=useritem[1])
        print(useritem[0], useritem[1], useritem[3], len(checkinouts))
        k = employee.objects.filter(name=useritem[3]).last()
        if k:
            l = extemployeeatt.objects.get_or_create(employeeid=k,
                                                     pin=useritem[1])
            print(l)
    return HttpResponse(len(checkinouts))


def checkeveryday(request):
    context = []
    body = 400
    daystart = datetime.datetime.strptime('2015-12-1', '%Y-%m-%d')
    dayend = datetime.datetime.strptime('2015-12-31', '%Y-%m-%d')

    eitems = checkinout.objects.filter(checktime__range=(daystart, dayend), userid=body).order_by('userid', 'checktime')
    context = eitems.values_list()
    # for i in eitems.values_list():
    #     print(i)
    lenday = dayend - daystart
    daytag = daystart
    while True:
        if daytag > dayend:
            break
        print(daytag)
        daytag += datetime.timedelta(days=1)

    print(lenday.days)
    print(daystart.year)
    print(daystart.month)
    print(daystart.day)
    print(len(eitems))

    # 方式
        #不打 为1
        #打   为1
        #和   为1
    # 设计班次
    # 天排班、周期
    # 人员周期内的排班表

    # 人员表
    # 计算得出每天状况
    # 产生全表
    # 汇总统计
    return HttpResponse(context)


def getmssql(request):
    import pymssql
    server = 'dba.jtanimation.com'
    user = 'attsql'
    password = 'qweasd123'
    conn = pymssql.connect(server, user, password, database='db_att2000')

    cursor = conn.cursor()
    cursor.execute("select * from CHECKINOUT where CHECKTIME >='2019-05-06'")
    row = cursor.fetchone()
    crows = []
    while row:
        crows.append(row)
        row = cursor.fetchone()

    print(len(crows))

    cursor = conn.cursor()
    cursor.execute('select * from userinfo')
    row = cursor.fetchone()
    prows = []
    while row:
        prows.append(row)
        row = cursor.fetchone()
    conn.close()

    uidpin = {}
    for prow in prows:
        uidpin[prow[0]] = prow[1]

    r = 0
    for userid, checktime, checktype, verifycode, sensorid, memoinfo, workcode, sn, userextfmt in crows:
        nitem = checkinout.objects.get_or_create(userid=userid,
                                                 checktime=checktime,
                                                 checktype=checktype,
                                                 verifycode=verifycode,
                                                 sensorid=sensorid,
                                                 memoinfo=memoinfo,
                                                 workcode=workcode,
                                                 sn=sn,
                                                 userextfmt=userextfmt,
                                                 pin = uidpin[userid])
        r += 1
        print(r)

    return HttpResponse(" 更新记录:" + str(r))


def getmssqlpin(request):
    import pymssql
    server = 'dba.jtanimation.com'
    user = 'attsql'
    password = 'qweasd123'
    conn = pymssql.connect(server, user, password, database='db_att2000')

    cursor = conn.cursor()
    cursor.execute('select * from userinfo')
    row = cursor.fetchone()
    prows = []
    while row:
        prows.append(row)
        row = cursor.fetchone()
    conn.close()

    for prow in prows:
        k = employee.objects.filter(name=prow[3])
        if k:
            l = extemployeeatt.objects.filter(employeeid=k.first())
            if l:
                # 更新
                l.update(pin=prow[1])
            else:
                # 新记录
                ttt = extemployeeatt.objects.get_or_create(employeeid=k.first(), pin=prow[1])
        else:
            print("+"*3, prow[3])
    r = u = 0

    return HttpResponse("已有记录: " + str(u) +" 更新记录:" + str(r))
