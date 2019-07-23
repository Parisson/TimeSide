#! /usr/bin/env python

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.core.management import call_command


class TestProvider(APITestCase):
    """ test item creation with providers """

    def setUp(self):
        user = User.objects.create_user(username='john',
                                        password='banana')
        token = Token.objects.get(user=user)
        call_command('timeside-create-boilerplate')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request_providers = self.client.get('/timeside/api/providers/', format='json')
        for provider in request_providers.data:
            if provider['pid'] == 'youtube':
                self.youtube_uuid = provider['uuid']
            if provider['pid'] == 'deezer':
                self.deezer_uuid = provider['uuid']
        
    def testProviderYoutubeFromURI(self):
        """ test item creation with youtube's MJ 'Beat It' track's URI """

        params = {'title':'Beat It',
                'description':'Music from Michael Jackson',
                'external_uri':'https://www.youtube.com/watch?v=oRdxUFDoQe0',
                'provider': '/timeside/api/providers/' + self.youtube_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testProviderYoutubeFromID(self):
        """ test item creation with youtube's MJ 'Beat It' track's ID """

        params = {'title':'Beat It',
                'description':'Music from Michael Jackson',
                'external_id':'oRdxUFDoQe0',
                'provider': '/timeside/api/providers/' + self.youtube_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testProviderDeezerFromURI(self):
        """ test item creation with Beatles' deezer's track's URI """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_uri':'https://www.deezer.com/fr/track/116348452',
                'provider': '/timeside/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testProviderDeezerFromID(self):
        """ test item creation with Beatles' deezer's track's ID """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_id':'116348452',
                'provider': '/timeside/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    

