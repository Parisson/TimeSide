#! /usr/bin/env python

from timeside.server.tests.timeside_test_server import TimeSideTestServer
from rest_framework import status

from django.conf import settings

import os

class TestProvider(TimeSideTestServer):
    """ test item creation with providers """

    def setUp(self):
        TimeSideTestServer.setUp(self)
        # self.items_url = reverse('')
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
        self.data = response.data

    def testProviderYoutubeFromID(self):
        """ test item creation with youtube's MJ 'Beat It' track's ID """

        params = {'title':'Beat It',
                'description':'Music from Michael Jackson',
                'external_id':'oRdxUFDoQe0',
                'provider': '/timeside/api/providers/' + self.youtube_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data = response.data

    def testProviderDeezerFromURI(self):
        """ test item creation with Beatles' deezer's track's URI """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_uri':'https://www.deezer.com/fr/track/116348452',
                'provider': '/timeside/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data = response.data

    def testProviderDeezerFromID(self):
        """ test item creation with Beatles' deezer's track's ID """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_id':'116348452',
                'provider': '/timeside/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/timeside/api/items/', params, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data = response.data

    def tearDown(self):
        if self.data['source_file']:
            os.remove(self.data['source_file'].replace('http://testserver/media/',settings.MEDIA_ROOT))