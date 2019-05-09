from django.db import models

# from hr.models import employee, employee_department
# Create your models here.


class extemployeeatt(models.Model):
    # 员工PIN
    employeeid = models.ForeignKey('hr.employee', on_delete=models.CASCADE, verbose_name='员工ID')
    pin = models.CharField(max_length=20, blank=True, null=True, verbose_name='pin')

    class Meta:
        db_table = 'att_extemployeeatt'


class classes(models.Model):
    # 班次
    name = models.CharField(max_length=24, blank=True, null=True, verbose_name='班次')
    type = models.IntegerField(default=0, verbose_name='type')

    class Meta:
        db_table = 'att_classes'


class timesolt(models.Model):
    # 时段
    name = models.CharField(max_length=16, verbose_name='时段')
    instar = models.TimeField(verbose_name='签到开始')
    intime = models.TimeField(verbose_name='签到时间')
    inend = models.TimeField(verbose_name='签到结束')
    incheck = models.FloatField(default=0, verbose_name='必须签到')

    class Meta:
        db_table = 'att_timesolt'


# class checkinout(models.Model):
#     # zktime8.5 db formate
#     userid = models.CharField(max_length=20, null=True, verbose_name='userid')
#     pin = models.CharField(max_length=20, blank=True, null=True, verbose_name='pin')
#     checktime = models.DateTimeField(blank=True, null=True, verbose_name='datatime')
#     checktype = models.CharField(max_length=5, blank=True, null=True, verbose_name='checktype')
#     verifycode = models.IntegerField(default=0, verbose_name='verifycode')
#     SN = models.CharField(max_length=20, blank=True, null=True, verbose_name='SN')
#     sensorid = models.CharField(max_length=5, blank=True, null=True, verbose_name='sensorid')
#     WorkCode = models.CharField(max_length=20, blank=True, null=True, verbose_name='WorkCode')
#     Reserved = models.CharField(max_length=20, blank=True, null=True, verbose_name='Reserved')
#     sn_name = models.CharField(max_length=40, blank=True, null=True, verbose_name='sn_name')
#
#     class Meta:
#         db_table = 'att_checkinout'


class checkinout(models.Model):
    # zktime5.0 db formate
    userid = models.IntegerField(default=0, verbose_name='userid')
    checktime = models.DateTimeField(blank=True, null=True, verbose_name='datatime')
    checktype = models.CharField(max_length=1, blank=True, null=True, verbose_name='checktype')
    verifycode = models.IntegerField(default=0, verbose_name='verifycode')
    sensorid = models.CharField(max_length=5, blank=True, null=True, verbose_name='sensorid')
    memoinfo = models.CharField(max_length=30, blank=True, null=True, verbose_name='memoinfo')
    workcode = models.CharField(max_length=20, blank=True, null=True, verbose_name='workcode')
    sn = models.CharField(max_length=20, blank=True, null=True, verbose_name='SN')
    userextfmt = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='userextfmt')
    pin = models.CharField(max_length=20, blank=True, null=True, verbose_name='pin')

    class Meta:
        db_table = 'att_checkinout'
