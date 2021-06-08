from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer

class TestResults(TimeSideTestServer):

    def test_get_hdf5(self):
        
        analyzer=Analysis.objects.get(
            title='f0 (aubio)'
        )
        analyzer.test=True
        analyzer.save()
        item=Item.objects.all()[0]

        param={
            "title": "string",
            "analysis": "/timeside/api/analysis/"+str(analyzer.uuid)+'/',
            "item": "/timeside/api/items/"+str(item.uuid)+'/'
        }
        analysis_track=self.client.post('/timeside/api/analysis_tracks/',param)
        result=self.client.get(analysis_track.data['result_url']+'visual/')
    
        print(result.content)

        
        
    def test_get_png(self):
        analyzer=Analysis.objects.get(
                title='Pitch grapher'
            )

        analyzer.test=True
        analyzer.save()
        item=Item.objects.all()[0]

        param={
            "title": "string",
            "analysis": "/timeside/api/analysis/"+str(analyzer.uuid)+'/',
            "item": "/timeside/api/items/"+str(item.uuid)+'/'
        }
        analysis_track=self.client.post('/timeside/api/analysis_tracks/',param)
        result=self.client.get(analysis_track.data['result_url']+'png/$')
    
        print(result.content)