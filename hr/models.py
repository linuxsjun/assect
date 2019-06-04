from django.db import models

# Create your models here.
# ==================员工表==================


class hrconfigs(models.Model):
    # 人力资源配置表
    name = models.CharField(max_length=32, null=True, verbose_name='配置名称')

    class Meta:
        db_table = 'hr_hrconfigs'


class department(models.Model):
    # 部门表
    pid = models.IntegerField(unique=True)
    name = models.CharField(max_length=32, null=False, verbose_name='名称')
    parentid = models.IntegerField(default=0, verbose_name='上级部门')
    order = models.IntegerField(null=True, verbose_name="次序")
    # 组织类型:0行政，1项目，2团队，3组织标签
    type = models.IntegerField(default=0, verbose_name='组织类型')
    wxsync = models.BooleanField(default=False, verbose_name="同步企业微信")

    class Meta:
        db_table = 'hr_department'


class employee(models.Model):
    # 员工表employee
    userid = models.CharField(unique=True, max_length=64, verbose_name='用户ID')
    employeeno = models.CharField(max_length=12, null=True, blank=True, verbose_name='员工编号')
    entry = models.DateField(null=True, blank=True, verbose_name='入职')
    leave = models.DateField(null=True, blank=True, verbose_name='离职')
    name = models.CharField(max_length=64, verbose_name='姓名')
    alias = models.CharField(null=True, blank=True, max_length=32, verbose_name='别名')
    department = models.CharField(null=True, blank=True, max_length=256, verbose_name='部门')
    position = models.CharField(null=True, blank=True, max_length=64, verbose_name='职务信息')
    mobile = models.CharField(null=True, blank=True, max_length=16, verbose_name='手机')
    # 性别，1    表示男性，2    表示女性
    gender = models.CharField(null=True, blank=True, max_length=16, verbose_name='姓别')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    # 头像url。注：如果要获取小图将url最后的”/0”改成”/100”即可。
    avatar = models.CharField(null=True, blank=True, max_length=256, verbose_name='头像')
    # 激活状态：1 = 已激活    2 = 已禁用    4 = 未激活    已激活代表已激活企业微信或已关注微工作台（原企业号）
    status = models.IntegerField(default=1, verbose_name="激活状态")
    # 成员启用状态。1表示启用的成员，0表示被禁用。服务商调用接口不会返回此字段
    enable = models.IntegerField(default=1, verbose_name="有效")
    # 上级字段，标识是否为上级。0表示普通成员，1表示上级
    isleader = models.IntegerField(default=0, verbose_name='主管')
    extattr = models.CharField(null=True, blank=True, max_length=256, verbose_name='扩展属性')
    hide_mobile = models.BooleanField(default=0, verbose_name='隐蔽手机')
    english_name = models.CharField(null=True, blank=True, max_length=64, verbose_name='英文名')
    telephone = models.CharField(null=True, blank=True, max_length=16, verbose_name='座机')
    order = models.CharField(null=True, blank=True, max_length=256, verbose_name='部门内的排序值')
    external_profile = models.CharField(null=True, blank=True, max_length=1024, verbose_name='成员对外属性')
    qr_code = models.CharField(null=True, blank=True, max_length=256, verbose_name='个人二维码')
    address = models.CharField(null=True, blank=True, max_length=128, verbose_name='地址')
    passwd = models.CharField(max_length=256, null=True, blank=True, verbose_name='密码')
    session = models.CharField(max_length=32, null=True, blank=True, verbose_name='Cookice_session')
    expsession = models.TimeField(null=True, blank=True)
    # 是否同步企业微信，F未同步，T已同步
    wxsync = models.BooleanField(default=0, verbose_name="同步企业微信")
    active = models.BooleanField(default=True, verbose_name='有效的')

    class Meta:
        db_table = 'hr_employee'


class extprivate(models.Model):
    employee_id = models.ForeignKey('employee', to_field='id', on_delete=models.CASCADE, related_name='privateid', verbose_name='员工ID')
    code = models.CharField(max_length=20, null=True, blank=True, verbose_name='身份证号')
    nationality = models.CharField(max_length=20, null=True, blank=True, verbose_name='国籍')
    nation = models.CharField(max_length=20, null=True, blank=True, verbose_name='民族')
    nationplace = models.CharField(max_length=20, null=True, blank=True, verbose_name='籍贯')
    birthday = models.DateField(verbose_name='生日')
    height = models.IntegerField(null=True, blank=True, verbose_name='身高')
    weight = models.IntegerField(null=True, blank=True, verbose_name='体重')
    blood = models.CharField(max_length=2, null=True, blank=True, verbose_name='血型')
    marital = models.BooleanField(default=False, verbose_name='婚姻')

    class Meta:
        db_table = 'hr_extprivate'


class extattr(models.Model):
    # 扩展属性
    empid = models.ForeignKey('employee', to_field='id', on_delete=models.CASCADE, related_name='employeeid', verbose_name='员工ID')
    # 类型 0：文本 1：网址 2：小程序
    type = models.IntegerField(default=0, verbose_name='类型')
    # 名称
    name = models.TextField(max_length=64, null=True, blank=True, verbose_name='名称')
    # 值
    value = models.TextField(max_length=256, null=True, blank=True, verbose_name='文本')
    url = models.TextField(max_length=256, null=True, blank=True, verbose_name='网址')
    title = models.CharField(max_length=64, null=True, blank=True, verbose_name='标题')

    class Meta:
        db_table = 'hr_extattr'


class employee_department(models.Model):
    # 员工部门关系表
    employeeid = models.ForeignKey('employee', to_field='userid', on_delete=models.CASCADE, verbose_name='员工ID')
    departmentid = models.ForeignKey('department', to_field='pid', on_delete=models.CASCADE, verbose_name='部门ID')
    isleader = models.BooleanField(default=0, verbose_name='负责人')

    class Meta:
        db_table = 'hr_employee_department'


class user_sign_log(models.Model):
    # 用户登录日志
    signtime = models.DateTimeField(verbose_name='登录时间')
    employeeid = models.ForeignKey('employee', on_delete=models.CASCADE, verbose_name='员工ID')
    fromip = models.CharField(max_length=16, verbose_name='来源IP')
    contl = models.CharField(max_length=32, verbose_name='描述或登录方式')

    class Meta:
        db_table = 'hr_user_sign_log'
