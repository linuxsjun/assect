# Generated by Django 2.1.1 on 2019-05-26 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='checkinout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(default=0, verbose_name='userid')),
                ('checktime', models.DateTimeField(blank=True, null=True, verbose_name='datatime')),
                ('checktype', models.CharField(blank=True, max_length=1, null=True, verbose_name='checktype')),
                ('verifycode', models.IntegerField(default=0, verbose_name='verifycode')),
                ('sensorid', models.CharField(blank=True, max_length=5, null=True, verbose_name='sensorid')),
                ('memoinfo', models.CharField(blank=True, max_length=30, null=True, verbose_name='memoinfo')),
                ('workcode', models.CharField(blank=True, max_length=20, null=True, verbose_name='workcode')),
                ('sn', models.CharField(blank=True, max_length=20, null=True, verbose_name='SN')),
                ('userextfmt', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='userextfmt')),
                ('pin', models.CharField(blank=True, max_length=20, null=True, verbose_name='pin')),
            ],
            options={
                'db_table': 'att_checkinout',
            },
        ),
        migrations.CreateModel(
            name='classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=24, null=True, verbose_name='班次')),
                ('type', models.IntegerField(default=0, verbose_name='type')),
            ],
            options={
                'db_table': 'att_classes',
            },
        ),
        migrations.CreateModel(
            name='classlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datestart', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('dateend', models.DateField(blank=True, null=True, verbose_name='结束日期')),
                ('adddate', models.DateTimeField(auto_now_add=True, verbose_name='新建时间')),
                ('moddate', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('active', models.BooleanField(default=True, verbose_name='有效的')),
                ('classid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.classes', verbose_name='班次ID')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee', verbose_name='员工ID')),
            ],
            options={
                'db_table': 'att_classlist',
            },
        ),
        migrations.CreateModel(
            name='classsolt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.classes')),
            ],
            options={
                'db_table': 'att_classsolt',
            },
        ),
        migrations.CreateModel(
            name='extemployeeatt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(blank=True, max_length=20, null=True, verbose_name='pin')),
                ('employeeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee', verbose_name='员工ID')),
            ],
            options={
                'db_table': 'att_extemployeeatt',
            },
        ),
        migrations.CreateModel(
            name='holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holidayname', models.CharField(max_length=20, verbose_name='节日名')),
                ('starttime', models.DateField(verbose_name='开始日期')),
                ('duration', models.IntegerField(default=1, verbose_name='持续天数')),
                ('holidaytype', models.IntegerField(default=2, verbose_name='类型')),
                ('quotient', models.IntegerField(default=2, verbose_name='系数')),
                ('active', models.BooleanField(default=True, verbose_name='有效的')),
            ],
            options={
                'db_table': 'att_holiday',
            },
        ),
        migrations.CreateModel(
            name='timesolt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='时段名')),
                ('instar', models.TimeField(verbose_name='签到开始')),
                ('intime', models.TimeField(verbose_name='签到时间')),
                ('inend', models.TimeField(verbose_name='签到结束')),
                ('incheck', models.BooleanField(default=True, verbose_name='必须签到')),
                ('inlate', models.IntegerField(default=0, verbose_name='迟到')),
                ('inabs', models.IntegerField(default=0, verbose_name='缺勤')),
                ('outstar', models.TimeField(verbose_name='签到开始')),
                ('outtime', models.TimeField(verbose_name='签到时间')),
                ('outend', models.TimeField(verbose_name='签到结束')),
                ('outcheck', models.BooleanField(default=True, verbose_name='必须签到')),
                ('outleave', models.IntegerField(default=0, verbose_name='早退')),
                ('outabs', models.IntegerField(default=0, verbose_name='缺勤')),
                ('ckeckoneall', models.BooleanField(verbose_name='签到一次即为全勤')),
                ('recday', models.IntegerField(default=1, verbose_name='记工作日')),
                ('recminute', models.IntegerField(default=30, verbose_name='记工作时')),
                ('lateif', models.BooleanField(default=False, verbose_name='迟到工时有效')),
                ('latetime', models.IntegerField(default=30, verbose_name='迟到以内')),
                ('sumworkhours', models.IntegerField(default=0, verbose_name='小计工时')),
                ('adddate', models.DateTimeField(auto_now_add=True, verbose_name='新建时间')),
                ('moddate', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'att_timesolt',
            },
        ),
        migrations.AddField(
            model_name='classsolt',
            name='timesoltid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.timesolt'),
        ),
    ]
