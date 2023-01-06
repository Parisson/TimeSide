#! /usr/bin/env python

from timeside.server.models import Item, Provider
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestProvider(TimeSideTestServer):
    #test that providers work and item creation with provider

    def test_youtube_provider_from_uri(self):
        youtube_provider = Provider.objects.get(pid = 'youtube')
        song_from_provider = Item.objects.create(
            provider = youtube_provider,
            title = "SevenDoors - Movement Of Whale (LGMX rework)",
            external_uri = 'https://www.youtube.com/watch?v=BMWpfG_Bpto&ab_channel=LGMX'
        )
        self.assertEqual(song_from_provider.get_uri(), "/srv/media/items/download/SevenDoors_-_Movement_Of_Whale_LGMX_rework-BMWpfG_Bpto.opus")
    
    def test_youtube_provider_from_id(self):
        youtube_provider = Provider.objects.get(pid = 'youtube')
        song_from_provider = Item.objects.create(
            provider = youtube_provider,
            title = "LGMX - Elevation (Para One rework)",
            external_id = 'REdstcbwstg'
        )
        self.assertEqual(song_from_provider.get_uri(), "/srv/media/items/download/LGMX_-_Elevation_Para_One_rework-REdstcbwstg.opus")
    

    def test_deezer_provider_from_uri(self):
        deezer_provider = Provider.objects.get(pid = 'deezer_preview')
        song_from_provider = Item.objects.create(
            provider = deezer_provider,
            title = "Raw",
            external_uri = 'https://www.deezer.com/en/track/823528792'
        )
        self.assertEqual(song_from_provider.get_uri(), "/srv/media/items/download/meute-raw-823528792.mp3")
    
    def test_deezer_provider_from_id(self):
        deezer_provider = Provider.objects.get(pid = 'deezer_preview')
        song_from_provider = Item.objects.create(
            provider = deezer_provider,
            title = "Raw",
            external_id = '823528792'
        )
        self.assertEqual(song_from_provider.get_uri(), "/srv/media/items/download/meute-raw-823528792.mp3")
   
    


class TestProviderRequests(TimeSideTestServer):
    """ test item creation with providers """

    def setUp(self):
        TimeSideTestServer.setUp(self)
        # self.items_url = reverse('')
        request_providers = self.client.get('/api/providers/', format='json')
        for provider in request_providers.data:
            if provider['pid'] == 'youtube':
                self.youtube_uuid = provider['uuid']
            if provider['pid'] == 'deezer_preview':
                self.deezer_uuid = provider['uuid']
        
       
    def testProviderYoutubeFromURI(self):
        """ test item creation with youtube's MJ 'Beat It' track's URI """

        params = {
                'title':"SevenDoors - Movement Of Whale (LGMX rework)",
                'external_uri':'https://www.youtube.com/watch?v=BMWpfG_Bpto&ab_channel=LGMX',
                'provider': '/api/providers/' + self.youtube_uuid + '/'
                }

        response = self.client.post('/api/items/', params, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['source_file'],None)

    def testProviderYoutubeFromID(self):
        """ test item creation with youtube's MJ 'Beat It' track's ID """

        params = {
                'title': "LGMX - Elevation (Para One rework)",
                'external_id':'REdstcbwstg',
                'provider': '/api/providers/' + self.youtube_uuid + '/'
                }

        response = self.client.post('/api/items/', params, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['source_file'],None)
        

    def testProviderDeezerFromURI(self):
        """ test item creation with Beatles' deezer's track's URI """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_uri':'https://www.deezer.com/fr/track/116348452',
                'provider': '/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/api/items/', params, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['source_file'],None)
        

    def testProviderDeezerFromID(self):
        """ test item creation with Beatles' deezer's track's ID """

        params = {'title':'Come Together',
                'description':'Music from The Beatles',
                'external_id':'116348452',
                'provider': '/api/providers/' + self.deezer_uuid + '/'
                }
        response = self.client.post('/api/items/', params, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['source_file'],None)
        

    