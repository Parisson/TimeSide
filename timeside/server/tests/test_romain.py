from timeside.core import processor
import h5py
from app.worker import app
from celery.contrib.testing.worker import start_worker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from timeside.server.models import *
from timeside.server.serializers import ProviderSerializer
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class test_romain(TimeSideTestServer):


    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        self.sweep_32000=Item.objects.get(title="sweep_32000")

    def test_youtube_dl(self):
        youtube_prov=Provider.objects.get(pid='youtube')
        data={'description': "Youtube Music from This Is It - Michael Jackson",
            'externalUri': "https://www.youtube.com/watch?v=oRdxUFDoQe0",
            'provider': "/timeside/api/providers/"+str(youtube_prov.uuid)+'/',
            'title': "Beat It"}
    

        item=self.client.post('/timeside/api/items/',data,format='json')
        print(item.content)

    def test_selection_title(self):
        sweeps=Item.objects.filter(title='sweep')
        sweeps_url=[]
        for s in sweeps :
            sweeps_url.append('timeside/api/items/'+str(s.uuid)+'/')
        data={
            #'title':'c la fete',
            'items': [],
            'author': '/timeside/api/users/admin/',
        }
        response=self.client.post('/timeside/api/selections/',data)
        print(response.content)
        



    def test_create_task(self):
        sweeps=Item.objects.filter(title='sweep')
        selection_sweep=Selection.objects.create()
        selection_sweep.items.set(sweeps)
        
        pitch_processor=Processor.objects.get(pid='aubio_pitch')
        pitch_preset=Preset.objects.create(processor=pitch_processor)
        experience=Experience.objects.create()
        experience.presets.add(pitch_preset)

        task=Task.objects.create(
            experience=experience,
            selection=selection_sweep,
            test=True
        )
        task.run()

        result_sweep0=Result.objects.get(
            item=sweeps[0],
            preset=pitch_preset
        )
        print(result_sweep0.has_file())
        print(result_sweep0.has_hdf5())

        hdf5=h5py.File(result_sweep0.hdf5,'r')
        print(hdf5.keys())
        print(hdf5['aubio_pitch.pitch'].keys())
        print(hdf5['aubio_pitch.pitch']['data_object'].keys())
        print(hdf5['aubio_pitch.pitch']['data_object']['value'][:])


    def test_create_analysis(self):
        print(str(a.preset.processor.pid) for a in Analysis.objects.all())
        preset=Preset.objects.get(
                processor=Processor.objects.get(pid='aubio_pitch'))
        analysis=Analysis.objects.get(preset=preset)
        analysis.test=True
        analysis.save()
        params = {'title':'test_analysis_'+str(analysis.uuid),
                'description':'',
                'analysis':'/timeside/api/analysis/'+str(analysis.uuid)+ '/',
                'item': '/timeside/api/items/' + str(self.sweep_32000.uuid) + '/',
                }
        analysis_track_response=self.client.post('/timeside/api/analysis_tracks/', params, format='json')
        result_response=self.client.get(analysis_track_response.data['result_url'],format='json')
        result=Result.objects.get(uuid=result_response.data['uuid'])

        print(result.has_file())
        print(result.has_hdf5())




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




       
    



