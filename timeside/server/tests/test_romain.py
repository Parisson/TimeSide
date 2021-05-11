import h5py
from app.worker import app
from celery.contrib.testing.worker import start_worker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from timeside.server.models import *
from timeside.server.serializers import ProviderSerializer
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class test_try(TimeSideTestServer):

    #allow_database_queries = True

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()

    #     # Start up celery worker
    #     cls.celery_worker = start_worker(app, perform_ping_check=False)
    #     cls.celery_worker.__enter__()

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()

    #     # Close worker
    #     cls.celery_worker.__exit__(None, None, None)

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        self.sweep_32000=Item.objects.get(title="sweep_32000")


    
    def test_analysis(self):
        
        pitch_analysis=Analysis.objects.get(title='Pitch')
        pitch_analysis.test=True
        pitch_analysis.save()

        
        params = {'title':'test_analysis',
                'description':'pitch on sweep_32000 for testing',
                'analysis':'/timeside/api/analysis/'+str(pitch_analysis.uuid)+ '/',
                'item': '/timeside/api/items/' + str(self.sweep_32000.uuid) + '/',
                }

        response = self.client.post('/timeside/api/analysis_tracks/', params, format='json')
        response_result_png=self.client.get(response.data['result_url'],format=json)
        print(response.status_code)

        pitch_preset=Preset.objects.get(
            processor=Processor.objects.get(pid='aubio_pitch')
            )

        result=Result.objects.get(
            item=self.sweep_32000,
            preset=pitch_preset
        )
       
        hdf5_file=h5py.File(result.hdf5,'r')
        print(hdf5_file.keys())
        print(hdf5_file['aubio_pitch.pitch_confidence']['data_object']['value'][:])

        

        response_hdf5= self.client.get('/timeside/api/results/'+str(result.uuid)+'/',format=json)
    
    def test_new_analysis(self):
        pitch_processor=Processor.objects.get(pid='aubio_pitch')
        pitch_subprocessor=SubProcessor.objects.create(processor=pitch_processor)
        pitch_preset=Preset.objects.create(processor=pitch_processor)
        pitch_analysis=Analysis.objects.create(
            sub_processor=pitch_subprocessor,
            preset=pitch_preset,
            test=True
        )
        params = {'title':'test_new_analysis',
                'description':'aubio_pitch on sweep_32000',
                'analysis':'/timeside/api/analysis/'+str(pitch_analysis.uuid)+ '/',
                'item': '/timeside/api/items/' + str(self.sweep_32000.uuid) + '/',
                }
        response = self.client.post('/timeside/api/analysis_tracks/', params, format='json')
        print(response.status_code)
        result=Result.objects.get(
            item=self.sweep_32000,
            preset=pitch_preset
        )
        response_result=self.client.get(response.data['result_url'],format=json)
        print(response_result.data)
        response_data=self.client.get('/timeside/results/'+str(result.uuid)+'/json/')
        print(response_data.data)

        
    def test_all_analysis(self):
        all_analysis=Analysis.objects.all()
        all_items=Item.objects.all()
        items=[]
        for i in range (8):
            items.append(Item.objects.get(uuid=all_items[i].uuid))
        c=0
        for a in all_analysis :
            a.test=True
            a.save()
            params = {'title':'test_all_analysis',
                'description':'',
                'analysis':'/timeside/api/analysis/'+str(a.uuid)+ '/',
                'item': '/timeside/api/items/' + str(items[c].uuid) + '/',
                }
            response = self.client.post('/timeside/api/analysis_tracks/', params, format='json')
            print(a.sub_processor.processor.pid)
            print(Result.objects.filter(item=items[c]))
            
            c+=1

      
        
        

    def test_item_request(self):
        
        sweep_32000=Item.objects.get(title="sweep_32000")
        item_url = reverse('item-detail', args=[sweep_32000.uuid])
        response = self.client.get(item_url, format='json')
        print(response.status_code)


    def test_get_waveform(self):

        waveform_processor=Processor.objects.get(pid="waveform_analyzer")
        waveform_preset=Preset.objects.get(processor=waveform_processor)
        waveform_experience=Experience.objects.create()
        waveform_experience.presets.add(waveform_preset)
        self.sweep_32000.run(waveform_experience)
        
        waveform_result=Result.objects.get(
            item=self.sweep_32000,
            preset=waveform_preset
            )
        waveform_result_file=h5py.File(waveform_result.hdf5,'r')
        print(waveform_result.has_hdf5())
        '''
        print(waveform_result_file['waveform_analyzer'].keys())
        print(waveform_result_file['waveform_analyzer']['data_object']['value'][:0])


        item_waveform_url = reverse('item-waveform', args=[self.sweep_32000.uuid])+"?format=json"
        print(item_waveform_url)
        response = self.client.get(item_waveform_url, format='json')
        print(response.status_code)
        print(response.data)
        '''




       
    



