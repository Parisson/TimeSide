from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from timeside.server.models import *
from django.db.utils import IntegrityError


from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestModels(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        #sweep_32000 will be the item use to test models
        self.sweep_32000=Item.objects.get(title="sweep_32000")
        self.youtube_provider=Provider.objects.get(pid='youtube')
        self.deezer_provider=Provider.objects.get(pid='deezer_preview')
    
    def test_uuid_unique(self):
        with self.assertRaises(IntegrityError):
            Item.objects.create(uuid=str(self.sweep_32000.uuid))

    def test_selection(self):
        item1=Item.objects.create()
        item2=Item.objects.create()
        selection=Selection.objects.create()
        selection.items.add(item1)
        selection.items.add(item1)
        selection.items.add(item2)
        all_items_id=[]
        for i in selection.get_all_items():
            all_items_id.append(i.uuid)
        self.assertIn(item1.uuid,all_items_id)
        self.assertIn(item2.uuid,all_items_id)
        self.assertEqual(2,len(all_items_id))


    def test_processor(self):
        processors_url="/timeside/api/processors/?format=json"
        response=self.client.get(processors_url,format='json')
        print(Processor.objects.all())


    def test_experience(self):
        pass




        
