# Generated by Django 2.1.4 on 2019-05-05 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('parentid', models.IntegerField(default=0, verbose_name='上级部门')),
                ('order', models.IntegerField(null=True, verbose_name='次序')),
                ('type', models.IntegerField(default=0, verbose_name='组织类型')),
                ('wxsync', models.BooleanField(default=False, verbose_name='同步企业微信')),
            ],
        ),
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=64, unique=True, verbose_name='用户ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('alias', models.CharField(blank=True, max_length=32, null=True, verbose_name='别名')),
                ('department', models.CharField(blank=True, max_length=256, null=True, verbose_name='部门')),
                ('position', models.CharField(blank=True, max_length=64, null=True, verbose_name='职务信息')),
                ('mobile', models.CharField(blank=True, max_length=16, null=True, verbose_name='手机')),
                ('gender', models.CharField(blank=True, max_length=16, null=True, verbose_name='姓别')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('avatar', models.CharField(blank=True, max_length=256, null=True, verbose_name='头像')),
                ('status', models.IntegerField(default=1, verbose_name='激活状态')),
                ('enable', models.IntegerField(default=1, verbose_name='有效')),
                ('isleader', models.IntegerField(default=0, verbose_name='主管')),
                ('extattr', models.CharField(blank=True, max_length=256, null=True, verbose_name='扩展属性')),
                ('hide_mobile', models.BooleanField(default=0, verbose_name='隐蔽手机')),
                ('english_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='英文名')),
                ('telephone', models.CharField(blank=True, max_length=16, null=True, verbose_name='座机')),
                ('order', models.CharField(blank=True, max_length=256, null=True, verbose_name='部门内的排序值')),
                ('external_profile', models.CharField(blank=True, max_length=1024, null=True, verbose_name='成员对外属性')),
                ('qr_code', models.CharField(blank=True, max_length=256, null=True, verbose_name='个人二维码')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='地址')),
                ('passwd', models.CharField(blank=True, max_length=256, null=True, verbose_name='密码')),
                ('session', models.CharField(blank=True, max_length=32, null=True, verbose_name='Cookice_session')),
                ('expsession', models.TimeField(blank=True, null=True)),
                ('wxsync', models.BooleanField(default=0, verbose_name='同步企业微信')),
                ('active', models.BooleanField(default=True, verbose_name='有效的')),
            ],
        ),
        migrations.CreateModel(
            name='employee_department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isleader', models.BooleanField(default=0, verbose_name='负责人')),
                ('departmentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.department', to_field='pid', verbose_name='部门ID')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee', to_field='userid', verbose_name='员工ID')),
            ],
        ),
        migrations.CreateModel(
            name='extattr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0, verbose_name='类型')),
                ('name', models.TextField(blank=True, max_length=64, null=True, verbose_name='名称')),
                ('value', models.TextField(blank=True, max_length=256, null=True, verbose_name='文本')),
                ('url', models.TextField(blank=True, max_length=256, null=True, verbose_name='网址')),
                ('empid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employeeid', to='hr.employee', verbose_name='员工ID')),
            ],
        ),
        migrations.CreateModel(
            name='hrconfigs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True, verbose_name='配置名称')),
            ],
        ),
        migrations.CreateModel(
            name='user_sign_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signtime', models.DateTimeField(verbose_name='登录时间')),
                ('fromip', models.CharField(max_length=16, verbose_name='来源IP')),
                ('contl', models.CharField(max_length=32, verbose_name='描述或登录方式')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee', verbose_name='员工ID')),
            ],
        ),
    ]
