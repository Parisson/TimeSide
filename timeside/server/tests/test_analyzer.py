from timeside.server.tests.timeside_test_server import TimeSideTestServer
from timeside.server.models import Analysis,Result,Item
import json

class TestAnalyzer(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        self.sweep_32000=Item.objects.get(title="sweep_32000")

    def test_analyzer(self):
        analyzers=Analysis.objects.all()
        analysis_sweep=[]
        for a in analyzers:
            self.analyzer_work_test(a.uuid)

    def analyzer_work_test(self, analysis_uuid):
        analysis=Analysis.objects.get(uuid=analysis_uuid)
        analysis.test=True
        analysis.save()

        params = {'title':'test_analysis_'+str(analysis_uuid),
                'description':'',
                'analysis':'/timeside/api/analysis/'+str(analysis_uuid)+ '/',
                'item': '/timeside/api/items/' + str(self.sweep_32000.uuid) + '/',
                }
        analysis_track_response=self.client.post('/timeside/api/analysis_tracks/', params, format='json')
        result_response=self.client.get(analysis_track_response.data['result_url'],format=json)
        result=Result.objects.get(uuid=result_response.data['uuid'])
        if analysis.render_type:
            self.assertTrue(result.has_file())
        else : self.assertTrue(result.has_hdf5())