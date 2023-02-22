from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer

class TestResults(TimeSideTestServer):

    def get_result(self, analyzer):
        
        analyzer.test = True
        analyzer.save()

        param = {
            "title": "string", 
            "analysis": "/api/analysis/" + str(analyzer.uuid) + '/',
            "item": self.item_url
        }
        analysis_track = self.client.post('/api/analysis_tracks/', param)
        self.assertEqual(analysis_track.status_code, 201)
        result = self.client.get(analysis_track.data['result_url'])
        self.assertEqual(result.status_code, 200)
        return result



    def test_get_hdf5(self):

        analyzer = Analysis.objects.get(
            title = 'F0 (aubio)'
        )
        
        result = self.get_result(analyzer)
        self.assertEqual(result.data['hdf5'][-5:], '.hdf5')

        
        
    def test_get_png(self):
        analyzer = Analysis.objects.get(
                title = 'Pitch grapher'
            )

        result = self.get_result(analyzer)    
        self.assertEqual(result.data['file'][-4:], '.png')



    def test_get_visual(self):
        analyzer = Analysis.objects.get(
            title = "Onsets (aubio)"
            )
        result = self.get_result(analyzer)
        self.assertEqual(result.data['hdf5'][-5:], '.hdf5')

        visual = self.client.get(result.data['url'] + "visual/")
        self.assertEqual(visual.content_type, 'image/png')




        




    
