from django.contrib import admin

from attendance.models import classes, classsolt, timesolt, checkinout, classlist
# Register your models here.

class timesolt_Admin(admin.ModelAdmin):
    list_display = ('name', 'instar', 'intime', 'inend', 'incheck', 'inlate', 'inabs', 'outstar', 'outtime', 'outend', 'outcheck', 'outleave', 'outabs', 'ckeckoneall', 'recday', 'recminute', 'lateif', 'latetime', 'sumworkhours', 'adddate', 'moddate' )
admin.site.register(timesolt, timesolt_Admin)


class classsolt_Admin(admin.ModelAdmin):
    list_display = ('classid', 'timesoltid')
admin.site.register(classsolt, classsolt_Admin)


class classes_Admin(admin.ModelAdmin):
    list_display = ('name', 'type')
admin.site.register(classes, classes_Admin)


class checkinout_Admin(admin.ModelAdmin):
    list_display = ('userid', 'checktime', 'checktype', 'verifycode', 'sensorid', 'memoinfo', 'workcode', 'sn', 'userextfmt', 'pin')
admin.site.register(checkinout, checkinout_Admin)


class classlist_Admin(admin.ModelAdmin):
    list_display = ('employeeid', 'classid', 'datestart', 'dateend', 'adddate', 'moddate')
admin.site.register(classlist, classlist_Admin)