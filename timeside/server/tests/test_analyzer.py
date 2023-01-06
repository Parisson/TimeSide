import json

from timeside.server.models import Analysis, Item, Result
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestAnalyzer(TimeSideTestServer):


    def test_analyzer(self):
        analyzers = Analysis.objects.all()
        for a in analyzers:
            self.analyzer_work_test(a)

    def analyzer_work_test(self, analysis):
        analysis.test = True
        analysis.save()

        params = {'title':'test_analysis_' + analysis.title, 
                'description':'', 
                'analysis':'/api/analysis/' + str(analysis.uuid) +  '/',
                'item': self.item_url, 
                }
        analysis_track_response = self.client.post('/api/analysis_tracks/', params, format = 'json')
        result_response = self.client.get(analysis_track_response.data['result_url'], format = json)
        result = Result.objects.get(uuid = result_response.data['uuid'])
        if analysis.render_type:
            self.assertTrue(result.has_file())
        else : 
            self.assertTrue(result.has_hdf5())
