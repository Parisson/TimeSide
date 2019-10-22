from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile

from timeside.core.tools.test_samples import generateSamples
from timeside.server.models import Item

import tempfile
import shutil

from timeside.server.tests.timeside_test_server import TimeSideTestServer


class ItemTests(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)

        # Generate test sample files
        self.samples_dir = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)
        self.samples = generateSamples(samples_dir=self.samples_dir)

        self.item_title = 'C4_scale'
        self.item_uuid = Item.objects.get(title=self.item_title).uuid
        
    def test_list_items(self):
        """
        Ensure we can get the list of items
        """
        item_list_url = reverse('item-list')
        response = self.client.get(item_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.samples))
        self.assertEqual(response.data[0].keys(),
                         ['uuid', 'url', 'title', 'description', 'player_url',
                          'source_file', 'source_url', 'mime_type'])

    def test_get_item(self):
        """
        Ensure we can get item object and related objects.
        """
        item_url = reverse('item-detail', args=[self.item_uuid])
        response = self.client.get(item_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data
        self.assertEqual(item.keys(),
                        ['uuid', 'url', 'player_url',
                        'title', 'description',
                        'source_file', 'source_url', 'mime_type',
                        'audio_url', 'audio_duration','external_uri',
                        'external_id',
                        'waveform_url',
                        'annotation_tracks',
                        'analysis_tracks',
                        'provider',
                        ])
        self.assertEqual(item['title'], self.item_title)

    def test_create_item(self):
        """
        Ensure we can create an item from an uploaded track.
        """
        item_create_url = reverse('item-list')

        for title in self.samples.keys():
            with open(self.samples[title], 'rb') as f:
                kwargs = {'title':title, 'source_file': f}
                response = self.client.post(item_create_url, kwargs, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        shutil.rmtree(self.samples_dir)

# class SelectionTests(APITestCase):

# class ExperienceTests(APITestCase):


class TaskTests(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)

        # Add presets duplicated from those from create-boilerplate
        proc_list_url = reverse('processor-list')
        response = self.client.get(proc_list_url, format='json')
        

    def test_task(self):
        pass



# class ProviderTests(APITestCase):

# class ResultTests(APITestCase):