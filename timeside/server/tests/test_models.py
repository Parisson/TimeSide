
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.conf import settings
from django.contrib.auth.models import User

from timeside.core.tools.test_samples import generateSamples
from timeside.server.models import Item

import tempfile
import shutil


class ItemTests(APITestCase):

    def setUp(self):
        # Generate test sample files
        self.samples_dir = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)
        self.samples = generateSamples(samples_dir=self.samples_dir)

        # Create test Items
        for title in self.samples.keys():
            Item.objects.create(title=title, source_file=self.samples[title])

        self.item_title = 'C4_scale.wav'
        self.item_uuid = Item.objects.get(title=self.item_title).uuid
        # Make all requests in the context of a logged in session.
        user = User.objects.create_user(username='john',
                                        password='banana')
        self.client.login(username='john', password='banana')
        
    def test_list_items(self):
        """
        Ensure we can get the list of items
        """
        item_list_url = reverse('item-list')
        response = self.client.get(item_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.samples))
        self.assertEqual(response.data[0].keys(),
                         ['uuid', 'url', 'title', 'description',
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
                         ['uuid', 'url', 'title', 'description',
                          'source_file', 'source_url', 'mime_type',
                          'audio_url', 'audio_duration',
                          'waveform_url',
                          'annotation_tracks',
                          'analysis_tracks', ])
        self.assertEqual(item['title'], self.item_title)

    def tearDown(self):
        shutil.rmtree(self.samples_dir)
