#! /usr/bin/env python

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.core.management import call_command


class TimeSideTestServer(APITestCase):
    """ Test class dealing with authentication and boilerplate """

    def setUp(self):
        call_command('timeside-create-admin-user', verbosity=0)
        call_command('timeside-create-boilerplate', verbosity=0)
        user = User.objects.get(username='admin')
        token = Token.objects.get(user=user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def tearDown(self):
        pass

    

