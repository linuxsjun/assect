from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),

    path('hr/', views.hr_list, name='employee'),
    path('hrdetailed/', views.hr_detailed, name='employee_detailed'),
    path('dep/', views.dep_list, name='department'),

    path('confbase/', views.confbase_view, name='config_base'),
    path('confmore/', views.confmore_view, name='config_more'),

    path('syncfromwx/', views.wx_syncfromwx),
    path('corpsecret/', views.wx_corpsecret_save),
]
