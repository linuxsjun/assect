from django.test import TestCase, Client
from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests, json

from base.models import configs
from hr.models import employee, department

# Create your tests here.

class dbTestCase(TestCase):
    def test_setUp(self):
        print('kkkkk')
        department.objects.create(pid=69, name='llllll', order=100001)
        print('kkkkk2')

    def test_check_dbTest(self):
        ps = department.objects.all()
        print(ps.count())
        # self.assertEqual(ps.name, 'The is ok')


class ATestCase(TestCase):
    # def index(request):
    #     ps = configs.objects.all().values()
    #     return HttpResponse(ps)


    def test_details(self):
        response = self.client.get('/hr/dep/')
        print('test---------')
        self.assertEqual(response.status_code, 200)


class indexTest(TestCase):
    def test_index(self):
        print('test---------1')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
