from django.contrib import admin

from hr.models import department, employee, employee_department

# Register your models here.

class employee_department_Admin(admin.ModelAdmin):
    list_display = ('employeeid', 'departmentid')
admin.site.register(employee_department, employee_department_Admin)

class department_Admin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'parentid', 'order')
admin.site.register(department, department_Admin)

class employee_Admin(admin.ModelAdmin):
    list_display = ('name','userid', 'department', 'position', 'mobile', 'session', 'active')
admin.site.register(employee, employee_Admin)