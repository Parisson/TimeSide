from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestAnalysisWithRequests(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        self.sweeps=Item.objects.filter(title='sweep')
    
    def test_subprocessor_requests(self):
        #listSubProcessors
        list_subprocessors=self.client.get('/timeside/api/subprocessors/', format='json')
        self.assertEqual(list_subprocessors.status_code, 200)
        self.assertEqual(len(list_subprocessors.data),SubProcessor.objects.count())
        
        #retrieveSubProcessor
        processor=self.client.get(list_subprocessors.data[0]['url'], format='json')
        self.assertEqual(processor.status_code, 200)
        
        #TODO: create a createSubProcessor request

    def delete_test(self,obj):
        delete_request=self.client.delete(obj.data['url'],format='json')
        self.assertEqual(delete_request.status_code,204)
        get_request=self.client.get(obj.data['url'],format='json')
        self.assertEqual(get_request.status_code,404)

    def test_analysis_requests(self):
        #listAnalysis
        list_analysis=self.client.get('/timeside/api/analysis/', format='json')
        self.assertEqual(list_analysis.status_code, 200)
        self.assertEqual(len(list_analysis.data),Analysis.objects.count())

        #createAnalysis
        list_subprocessors=self.client.get('/timeside/api/subprocessors/', format='json')
        subprocessor=self.client.get(list_subprocessors.data[0]['url'], format='json')

        list_presets=self.client.get('/timeside/api/presets/', format='json')
        preset=self.client.get(list_presets.data[0]['url'], format='json')
        
        data={
            'title':'test_analysis',
            'preset':preset.data['url'],
            'sub_processor':subprocessor.data['url'],
            "parameters_schema": { }
        }
        analysis=self.client.post('/timeside/api/analysis/',data,format='json')
        self.assertEqual(analysis.status_code,201)

        #retrieveAnalysis
        self.assertEqual(self.client.get(analysis.data['url'], format='json').status_code,200)

        #update
        data['title']='test_analysis_update'
        analysis=self.client.put(analysis.data['url'], data, format='json')
        self.assertEqual(analysis.data['title'],data['title'])

        #delete
        self.delete_test(analysis)
        
        

    def test_analysistrack_requests(self):
        #listAnalysisTracks
        list_analysis_tracks=self.client.get('/timeside/api/analysis_tracks/', format='json')
        self.assertEqual(list_analysis_tracks.status_code, 200)
        self.assertEqual(len(list_analysis_tracks.data),AnalysisTrack.objects.count())

        #getAnalysis
        analysis_obj=Analysis.objects.get(
            sub_processor=SubProcessor.objects.get(
                processor=Processor.objects.get(pid='aubio_pitch')
        ))
        analysis_obj.test=True
        analysis_obj.save()
        analysis=self.client.get('/timeside/api/analysis/'+str(analysis_obj.uuid)+'/', format='json')

        #createAnalysisTrack
        data={
            'title':'test_analysis_track',
            'description':'',
            'analysis':analysis.data['url'],
            'item':self.client.get('/timeside/api/items/', format='json').data[0]['url']
        }
        analysis_track=self.client.post('/timeside/api/analysis_tracks/',data,format='json')
        self.assertEqual(analysis_track.status_code,201)

        #check result_url
        result=self.client.get(analysis_track.data['result_url'], format='json')
        self.assertEqual(result.status_code,200)

        #retrieveAnalysisTrack
        self.assertEqual(self.client.get(analysis_track.data['url'], format='json').status_code,200)

        #update : change item
        data['item']=self.client.get('/timeside/api/items/', format='json').data[1]['url']
        analysis_track=self.client.put(analysis_track.data['url'], data, format='json')
        self.assertEqual(analysis_track.data['item'],data['item'])
        
        result=self.client.get(analysis_track.data['result_url'], format='json')
        self.assertEqual(result.data['item'],data['item'])
        
        #update : change analysis
        analysis_obj=Analysis.objects.get(
            sub_processor=SubProcessor.objects.get(
                processor=Processor.objects.get(pid='aubio_silence')
        ))
        analysis_obj.test=True
        analysis_obj.save()
        analysis=self.client.get('/timeside/api/analysis/'+str(analysis_obj.uuid)+'/', format='json')

        data['analysis']=analysis.data['url']
        analysis_track=self.client.put(analysis_track.data['url'], data, format='json')
        self.assertEqual(analysis_track.data['analysis'],data['analysis'])
        
        result=self.client.get(analysis_track.data['result_url'], format='json')
        self.assertEqual(result.data['preset'],analysis.data['preset'])

        #delete
        self.delete_test(analysis_track)
