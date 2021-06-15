from django.test.client import BOUNDARY,  MULTIPART_CONTENT,  encode_multipart
from timeside import __file__ as ts_file
from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestItem(TimeSideTestServer):


    def test_get_items_list(self):
        items = self.client.get('/timeside/api/items/', format = 'json')
        self.assertEqual(items.status_code, 200)
        self.assertEqual(len(items.data), Item.objects.count())
    
    def test_get_item(self):
        item = self.client.get(self.item_url, format = 'json')
        self.assertEqual(item.status_code, 200)
        self.assertEqual(item.data['uuid'], str(self.item.uuid))

    def test_create_item_from_url(self):
        lgmx_mp3_url = "https://www.lgmx.fr/main/audio/LGMX-Elevation.mp3"
        data = {
            "title": "LGMX-Elevation", 
            "description": "mp3 from lgmx website", 
            "source_url": lgmx_mp3_url, 
        }
        item = self.client.post('/timeside/api/items/',  data,  format = 'json')
        self.assertEqual(item.status_code,  201)
        self.assertEqual(item.data['source_file'], None)
        self.assertEqual(item.data['source_url'], lgmx_mp3_url)
        
        item_obj = Item.objects.get(uuid = item.data['uuid'])
        item_obj.run(self.experience)

    def test_create_item_with_local_song(self):
        ts_path = os.path.split(os.path.abspath(ts_file))[0]
        tests_dir = os.path.abspath(os.path.join(ts_path, '../tests'))
        tests_dir += '/samples/sweep.flac'
        f = open(tests_dir, 'rb')
        data = encode_multipart(BOUNDARY, {
            "title": "test_create_item_from_local_song", 
            "description": "sweep.mp3 from local test directory", 
            'source_file': f
        })
        item = self.client.post('/timeside/api/items/', data, content_type = MULTIPART_CONTENT)
        self.assertEqual(item.status_code,  201)
        self.assertEqual(item.data['source_file'][-5:], '.flac')

        item_obj = Item.objects.get(uuid = item.data['uuid'])
        item_obj.run(self.experience)


    def test_update_item(self):

        data = {
            'title':'this_is_a_test'
        }
        item = self.client.put(self.item_url, data, format = 'json')
        self.assertEqual(item.status_code, 200)
        self.assertEqual(item.data['title'], data['title'])
        

    def test_delete_item(self):
        delete_request = self.client.delete(self.item_url, format = 'json')
        self.assertEqual(delete_request.status_code, 204)
        get_request = self.client.get(self.item_url, format = 'json')
        self.assertEqual(get_request.status_code, 404)


    def test_get_waveform(self):
        item = self.client.get(self.item_url)
        waveform = self.client.get(item.data['waveform_url'])
        self.assertEqual(waveform.status_code, 200)
        self.assertIn('waveform', waveform.data.keys())

    def test_download(self):
        file=self.client.get(self.item_url + 'download/flac')
        print(file.content)


    

