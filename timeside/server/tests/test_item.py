from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY


class TestItemRequests(TimeSideTestServer):

    def test_item_run_experience(self):
        pass

    def test_item_get_source(self):
        pass

    def test_item_get_external_id(self):
        pass

    def test_item_get_uri(self):
        pass

    def test_item_get_results_path(self):
        pass

    def test_item_get_audio_info(self):
        pass

    def test_item_get_hash(self):
        pass

    def test_item_get_mimetype(self):
        pass



class TestItemWithRequests(TimeSideTestServer):

    def obj_url(self,obj):
        return '/timeside/api/items/'+str(obj.uuid)+'/'

    def test_get_items_list(self):
        items=self.client.get('/timeside/api/items/',format='json')
        self.assertEqual(items.status_code,200)
        self.assertEqual(len(items.data),Item.objects.count())
    
    def test_get_item(self):
        item_obj=Item.objects.all()[0]
        item=self.client.get(self.obj_url(item_obj),format='json')
        self.assertEqual(item.status_code,200)
        self.assertEqual(item.data['uuid'],str(item_obj.uuid))

    def test_create_item_from_url(self):
        lgmx_mp3_url="https://www.lgmx.fr/main/audio/LGMX-Elevation.mp3"
        data={
            "title": "LGMX-Elevation",
            "description": "mp3 from lgmx website",
            "source_url": lgmx_mp3_url,
        }
        item=self.client.post('/timeside/api/items/', data, format='json')
        self.assertEqual(item.status_code, 201)
        self.assertEqual(item.data['source_file'],None)
        
        item_obj=Item.objects.get(uuid=item.data['uuid'])
        experience=Experience.objects.create()
        experience.presets.add( 
            Preset.objects.create(
                processor=Processor.objects.get(pid='aubio_pitch')
            )
        )
        item_obj.run(experience)

    def test_create_item_with_local_song(self):
        from timeside import __file__ as ts_file
        ts_path = os.path.split(os.path.abspath(ts_file))[0]
        tests_dir = os.path.abspath(os.path.join(ts_path, '../tests'))
        tests_dir+='/samples/sweep.flac'
        f = open(tests_dir, 'rb')
        data=encode_multipart(BOUNDARY,{
            "title": "test_create_item_from_local_song",
            "description": "sweep.mp3 from local test directory",
            'source_file': f
        })
        item=self.client.post('/timeside/api/items/', data, content_type=MULTIPART_CONTENT)
        self.assertEqual(item.status_code, 201)
        self.assertEqual(item.data['source_file'][-5:],'.flac')

        item_obj=Item.objects.get(uuid=item.data['uuid'])
        experience=Experience.objects.create()
        experience.presets.add( 
            Preset.objects.create(
                processor=Processor.objects.get(pid='aubio_pitch')
            )
        )
        item_obj.run(experience)


    def test_update_item(self):
        item_obj=Item.objects.all()[0]
        item=self.client.get(self.obj_url(item_obj),format='json')

        #update title
        data={
            'title':'this_is_a_test'
        }
        item=self.client.put(item.data['url'],data,format='json')
        self.assertEqual(item.status_code,200)
        self.assertEqual(item.data['title'],data['title'])
        
        #update song
        #TODO

    def test_delete_item(self):
        item_obj=Item.objects.all()[0]
        delete_request=self.client.delete(self.obj_url(item_obj),format='json')
        self.assertEqual(delete_request.status_code,204)
        get_request=self.client.get(self.obj_url(item_obj),format='json')
        self.assertEqual(get_request.status_code,404)


    def test_get_waveform(self):
        item_obj=Item.objects.get(title="sweep_32000")
        item=self.client.get(self.obj_url(item_obj))
        waveform=self.client.get(item.data['waveform_url'])
        self.assertEqual(waveform.status_code, 200)
        self.assertIn('waveform',waveform.data.keys())


    

