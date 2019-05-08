from django.test import TestCase, Client

from django.http import HttpResponse

from hr.models import hrconfigs

import requests
from requests.exceptions import RequestException
import re
import threading
import time

# Create your tests here.
def getpinyin(chinastr):
    url = 'https://www.qqxiuzi.cn/zh/pinyin/show.php'
    data = {
        't': chinastr,
        'd': 3
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    # data =data.encode('utf-8')
    try:
        s = requests.session()
        req = s.post(url, data=data, headers=header)
        if req.status_code == 200:
            if req.text:
                # print(req.text)
                pattern = re.compile('e">(.*?)</', re.S)
                pinyin = re.search(pattern, req.text)
                # print(pinyin.group(0))
                return pinyin.group(1)
        return None
    except RequestException:
        print('请求PINYIN页面失败')
        return None


def thread_job_l1():
    for i in range(5):
        print("this an added Thread1, number is %s" % threading.current_thread())
        time.sleep(1)
    print("jobs l1 finish")


def thread_job_l2():
    for i in range(5):
        print("this an added Thread2, number is %s" % threading.current_thread())
        time.sleep(2)
    print("jobs l2 finish")


class indexTest(TestCase):
    def setUp(self) -> None:
        print("********** hr test **********")

    def test_getpinyin(self):
        print('======== test getpinyin =========')
        cnstr = '务必'
        getbk = getpinyin(cnstr)
        print('"%s" pinyin is %s' % (cnstr, getbk))


    def test_threadss(self):
        print('======== test threading =========')
        add_thread = threading.Thread(target=thread_job_l1)
        add_thread2 = threading.Thread(target=thread_job_l2)
        add_thread.start()
        add_thread2.start()

        print(threading.active_count())
        print(threading.enumerate())
        print(threading.current_thread())

        while True:
            if len(threading.enumerate()) <= 1:
                break
        print('all done')


    def test_db_hrconfigs(self):
        print('======== test db hrconfig =========')
        ndb = hrconfigs(name='kkkk')
        ndb.save()
        self.assertEqual(ndb.name, 'kkkk')


    def test_vdeplist(self):
        csrf_client = Client(enforce_csrf_checks=True)
        print('======== test v dep list =========')
        response = csrf_client.post('/sign/', {'user': 'admin', 'passwd': ''})
        print(response.status_code)
        print(response.content)
        response = csrf_client.get('/hr/dep/')
        print(response.status_code)
        response.encoding = 'UTF-8'
        print(response.content)
        self.assertEqual(response.status_code, 200)


    def tearDown(self) -> None:
        print('********** end hr test **********')
