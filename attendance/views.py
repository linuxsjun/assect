from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Max, Min, Count

from attendance.models import extemployeeatt, holiday, classlist, classes, classsolt, timesolt, checkinout
from hr.models import employee

import datetime
import time
import threading
from xml.etree.ElementTree import parse

# Create your views here.
def index(request):
    return redirect('/att/attendance/')


def attendance(request):
    context = {}
    context['title'] = '签到'

    if request.method == "GET":
        # print('get')
        if "namecheck" in request.GET:
            employeename = request.GET['namecheck']
            if employeename == '':
                pass
        if 'datecheck' in request.GET:
            datecheck = request.GET['datecheck']
            daytoday = datetime.datetime.strptime(datecheck, '%Y-%m-%d')
        else:
            daytoday = datetime.datetime.today()
        if 'departmentcheck' in request.GET:
            department = request.GET['departmentcheck']
            if department == '':
                pass
        if 'getdays' in request.GET:
            pass

    context['daytoday'] = daytoday

    d = []
    pindicts= {}
    # 查找PIN
    # emppins = employee.objects.all() \
    emppins = employee.objects.exclude(extemployeeatt__pin=None) \
        .order_by('employee_department__departmentid__name', 'name')\
        .values('name', 'extemployeeatt__pin', 'employee_department__departmentid__name')
    print(len(emppins))
    for emppin in emppins:
        pindicts[emppin['extemployeeatt__pin']] = emppin
        print(emppin)

    # # 查找班次
    # ks = classlist.objects.all() \
    #     .values('id',
    #             'employeeid',
    #             'classid__name',
    #             'employeeid__extemployeeatt__pin',
    #             'datestart',
    #             'dateend') \
    #     .order_by('datestart')
    # print(ks)

    # 填写一览
    ps = checkinout.objects.filter(checktime__year=daytoday.year,
                                   checktime__month=daytoday.month,
                                   checktime__day=daytoday.day) \
        .values('pin') \
        .annotate(last=Max('checktime'), fast=Min('checktime'), count=Count('userid'))

    for p in ps:
        i = {}
        if p['pin'] in pindicts:
            i.update(pindicts[p['pin']])
        i.update(p)
        i['long'] = i['last'] - i['fast']
        d.append(i)
        # print(i)
    context['context2'] = d

    # ps = checkinout.objects.filter(checktime__year=daytoday.year,
    #                                checktime__month=daytoday.month,
    #                                checktime__day=daytoday.day,
    #                                pin=32).values().order_by('-checktime')
    # emppins = employee.objects.exclude(extemployeeatt__pin=None)\
    #     .order_by('employee_department__departmentid__name', 'name')\
    #     .values('name', 'extemployeeatt__pin', 'employee_department__departmentid__name')
    # pinsdict = {}
    # for i in emppins:
    #     pinsdict[i['extemployeeatt__pin']] = i
    #     del pinsdict[i['extemployeeatt__pin']]['extemployeeatt__pin']
    # p = []
    # for k in ps:
    #     if k['pin']:
    #         if k['pin'] in pinsdict:
    #             k.update(pinsdict[k['pin']])
    #     p.append(k)
    # context['context'] = p


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

    ps = classlist.objects.all()\
        .values('employeeid_id',
                 'employeeid__name',
                 'employeeid__employee_department__departmentid__name',
                 'employeeid__extemployeeatt__pin',
                 'classid__name',
                 'datestart',
                 'dateend',
                 'active').order_by('employeeid_id', 'employeeid__employee_department__departmentid__name', 'datestart')
    context['context'] = ps

    return render(request, 'att_class_board.html', context)


def attholiday(request):
    context={}
    context['title'] = '假期'
    return render(request, 'att_holiday_board.html', context)


def configatt(request):
    context={}
    context['title'] = '设置'
    return render(request, 'attendance_conf.html', context)


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
    cursor.execute("select * from CHECKINOUT where CHECKTIME >='2019-05-11'")
    # cursor.execute("select * from CHECKINOUT")
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
                                                 pin=uidpin[userid])
        m, n = nitem
        if n:
            r += 1
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


def cmpcheck(request):
    employeeid = 17
    checkday = datetime.datetime.strptime('2019-4-1', '%Y-%m-%d')

    datestart = datetime.datetime.strptime('2019-4-1', '%Y-%m-%d')
    dateend = datetime.datetime.strptime('2019-4-30', '%Y-%m-%d')

    # 计算工作日 ==========================
    holidays = holiday.objects.filter(starttime__range=[datestart, dateend]).values().order_by('starttime')

    thisdate = datestart
    ppds=[]
    while thisdate <= dateend:
        ee = {}
        ee['employeeid'] = employeeid
        ee['daycheck'] = thisdate
        ee['weekday'] = thisdate.weekday()
        ee['autopb'] = True

        # 周末计算
        if (ee['weekday'] == 5) or (ee['weekday'] == 6):
            ee['workday'] = False
            ee['quot'] = 1
        else:
            ee['workday'] = True
            ee['quot'] = 0
        thisdate += datetime.timedelta(days=1)
        ppds.append(ee)

    #  节假日更新
    for hday in holidays:
        firsday = datetime.datetime.strptime(str(hday['starttime']), '%Y-%m-%d')
        adddays = hday['duration']
        quotient = hday['quotient']
        endday = firsday + datetime.timedelta(days=(adddays-1))
        for pb in ppds:
            if (pb['daycheck'] >= firsday) and (pb['daycheck'] <= endday):
                if quotient == 0:
                    pb['workday'] = True
                else:
                    pb['workday'] = False
                pb['quot'] = quotient

    # =======================
    # 填写班次
    chcemployee = employee.objects.get(pk=employeeid)
    ks = classlist.objects.filter(employeeid=chcemployee) \
        .values('id',
                'classid',
                'classid__name',
                'employeeid__name',
                'employeeid__extemployeeatt__pin',
                'datestart',
                'dateend')\
        .order_by('employeeid', 'datestart')
    print(ks)


    for pb in ppds:
        thisdate = pb['daycheck']
        if pb['workday'] and ks:
            for k in ks:
                # pb['pin'] = k['employeeid__extemployeeatt__pin']
                sr = datetime.datetime.strptime(str(k['datestart']), "%Y-%m-%d")
                sp = datetime.datetime.strptime(str(k['dateend']), "%Y-%m-%d")
                if (thisdate >= sr) and (thisdate <= sp):
                    pb['classes'] = k['classid']
                    pb['classname'] = k['classid__name']
        else:
            pb['classes'] = 0
            pb['classname'] = None
        print(pb)

    # =======================


    # 计算步骤
    # 计算排班
    chcemployee = employee.objects.get(pk=employeeid)
    # k = classlist.objects.filter(employeeid=chcemployee)\
    k = classlist.objects.all() \
        .values('id',
                'employeeid',
                'employeeid__name',
                'employeeid__extemployeeatt__pin',
                'datestart',
                'dateend',
                'classid__classsolt__timesoltid_id',
                'classid__classsolt__timesoltid_id__name',
                'classid__classsolt__timesoltid_id__intime')\
        .order_by('employeeid', 'datestart')

    timequery = timesolt.objects.all().values()
    timedicts = {}
    for i in timequery:
        timedicts[i['id']] = i

    # 根据排班规则自动排班
    emppbs = []
    for i in k:
        # print(i)
        e = i['datestart'].strftime("%Y-%m-%d")
        sr = datetime.datetime.strptime(e, "%Y-%m-%d")

        e = i['dateend'].strftime("%Y-%m-%d")
        sp = datetime.datetime.strptime(e, "%Y-%m-%d")

        thisdate = datestart
        while thisdate <= dateend:
            pb = {}
            pb['employeeid'] = i['employeeid']
            pb['daycheck'] = thisdate
            pb['pin'] = i['employeeid__extemployeeatt__pin']
            pb['weekday'] = thisdate.weekday()
            pb['autopb'] = True
            if (thisdate >= sr)and(thisdate <= sp):
                pb['timesoltid'] = i['classid__classsolt__timesoltid_id']
            else:
                pb['timesoltid'] = 0
            emppbs.append(pb)
            thisdate += datetime.timedelta(days=1)

    # 根据周末数据，校正周末排班
    # 工作日为0，公休日1，节假日2
    for pb in emppbs:
        if (pb['weekday'] == 5) or (pb['weekday'] == 6):
            pb['timesoltid'] = 0
            pb['quot'] = 1
        else:
            # pb.update(timedicts[i['classid__classsolt__timesoltid_id']])
            pb['quot'] = 0
        # print(pb)

    #  根据节假日数据，校正节假日排班
    holidays = holiday.objects.filter(starttime__range=[datestart, dateend]).values().order_by('starttime')
    # print(len(holidays))
    for hday in holidays:
        firsday = datetime.datetime.strptime(str(hday['starttime']), '%Y-%m-%d')
        adddays = hday['duration']
        quotient = hday['quotient']
        endday = firsday + datetime.timedelta(days=(adddays-1))

        for pb in emppbs:
            if (pb['daycheck'] >= firsday) and (pb['daycheck'] <= endday):
                pb['timesoltid'] = 0
                pb['quot'] = quotient

    # print(len(emppbs))

    # 根据单据校正打卡规则及时段时间
    pass

    # 根据排班表提取当时数据
    ps = checkinout.objects.filter(checktime__range=[datestart, dateend]) \
        .values_list('id', 'pin', 'checktime')\
        .order_by('checktime')
    # print(len(ps))

    for pb in emppbs:
        if pb['timesoltid'] != 0:
            pb['ckecktimes'] = []
            for checkt in ps.filter(checktime__year=pb['daycheck'].year, checktime__month=pb['daycheck'].month, checktime__day=pb['daycheck'].day, pin=pb['pin']):
                pb['ckecktimes'].append(checkt[2])
        # print(pb)

    # 找到对应数据，计算规所需的对应源数据
    # 使用源数据，核对规则
    # 计算出结果并保存进表格
    # kkk=llll
    return HttpResponse("ok")
