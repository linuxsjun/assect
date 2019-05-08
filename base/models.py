from django.db import models

# Create your models here.

#==================基本表==================
class configs(models.Model):
    #基础设置
    companycode = models.CharField(max_length=128, null=True, blank=True, verbose_name='企业编码')
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='企业名称')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='地址')
    postal = models.CharField(max_length=8, null=True, blank=True, verbose_name='邮政编码')
    tel = models.CharField(max_length=16, null=True, blank=True, verbose_name='电话')
    fex = models.CharField(max_length=16, null=True, blank=True, verbose_name='传真')
    web = models.CharField(max_length=128, null=True, blank=True, verbose_name='网址')
    mail = models.CharField(max_length=32, null=True, blank=True, verbose_name='邮箱')

    # 开票信息

    # 微信设置
    corpid = models.CharField(max_length=128, null=True, verbose_name='企业ID')

    # class Meta:
    #     db_table = 'base_config'

class wxsecret(models.Model):
    #微信密钥配置表
    name = models.CharField(max_length=32, null=True, verbose_name='名称')
    agentid = models.IntegerField(null=True, verbose_name='微信应用ID')
    corpsecret = models.CharField(max_length=64,null=True, verbose_name='API密钥')
    token = models.CharField(max_length=256, null=True, verbose_name='Token')
    expirestime = models.DateTimeField(null=True, blank=True, verbose_name='到期时间')

    # class Meta:
    #     db_table = 'base_wxsecret'