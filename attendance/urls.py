from django.urls import path

from . import views

app_name = 'attendance'
urlpatterns = [
    path('', views.index, name='index'),

    path('attendance/', views.attendance, name='attendance'),
    path('attclass/', views.attclass, name='attclass'),
    path('holiday/', views.attholiday, name='holiday'),
    path('summary/', views.summary, name='summary'),
    path('att_collect_detail/', views.att_collect_detail, name='collect'),

    path('confatt/', views.configatt, name='config'),

    path('inputxml/', views.inputxml),
    path('checkbody/', views.checkeveryday),
    path('getmssql/', views.getmssql),
    path('getmssqlpin/', views.getmssqlpin),
    path('cmpcheck/', views.cmpcheck),
]
