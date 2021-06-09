#! /usr/bin/env python

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from timeside.server.models import *

from django.contrib.auth.models import User
from django.core.management import call_command

# from celery.contrib.testing.worker import start_worker


class TimeSideTestServer(APITestCase):
    """ Test class dealing with authentication and boilerplate """

    def setUp(self):
        call_command('timeside-create-admin-user', verbosity=0)
        call_command('timeside-create-boilerplate', verbosity=0)
        user = User.objects.get(username='admin')
        token = Token.objects.get(user=user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.login(username='admin', password='admin')
        
        #values
        self.item=Item.objects.get(source_file='items/tests/sweep.wav')
        self.item_url='/timeside/api/items/'+str(self.item.uuid)+'/'
        self.item2=Item.objects.get(source_file='items/tests/sweep.mp3')
        self.item2_url='/timeside/api/items/'+str(self.item2.uuid)+'/'

        self.selection=Selection.objects.create()
        self.selection.items.set([self.item])
        self.selection_url='/timeside/api/selections/'+str(self.selection.uuid)+'/'


        self.processor=Processor.objects.get(pid='aubio_pitch')
        self.processor_url='/timeside/api/processors/aubio_pitch/'
        self.processor2=Processor.objects.get(pid='aubio_silence')
        self.processor2_url='/timeside/api/processors/aubio_silence/'

        self.preset=Preset.objects.create(processor=self.processor)
        self.preset_url='/timeside/api/presets/'+str(self.preset.uuid)+'/'
        self.preset2=Preset.objects.create(processor=self.processor2)
        self.preset2_url='/timeside/api/presets/'+str(self.preset2.uuid)+'/'

        self.experience=Experience.objects.create()
        self.experience.presets.add(self.preset)
        self.experience_url='/timeside/api/experiences/'+str(self.experience.uuid)+'/'

        self.analysis=Analysis.objects.get(
            sub_processor=SubProcessor.objects.get(
                processor=self.processor)
            )
        self.analysis.test=True
        self.analysis.save()
        self.analysis_url='/timeside/api/analysis/'+str(self.analysis.uuid)+'/'


    def delete_test(self,obj):
        delete_request=self.client.delete(obj.data['url'],format='json')
        self.assertEqual(delete_request.status_code,204)
        get_request=self.client.get(obj.data['url'],format='json')
        self.assertEqual(get_request.status_code,404)

        


        



    

