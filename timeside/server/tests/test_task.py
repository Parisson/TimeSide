from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestTask(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)

    def test_simple_task(self):

        task=Task.objects.create(
            experience=self.experience,
            item=self.item,
            test=True
        )
        task.run()
        result=Result.objects.get(
            preset=self.preset,
            item=self.item
        )
        self.assertTrue(result.has_hdf5())


    def test_all_processors(self):
        pass
        #TODO : why 7 processors do not work ?
        """ 

        all_processors=Processor.objects.all()
        all_presets=[]
        for p in all_processors:
            all_presets.append(Preset.objects.create(processor=p))
            
        all_processors_experience=Experience.objects.create()
        all_processors_experience.presets.set(all_presets)
        sweep_selection=Selection.objects.create()

        #add sweep.ogg, sweep.flac, sweep.mp3 and sweep.wav
        sweep_selection.items.set(self.sweeps[:1])
        task=Task.objects.create(
            experience=all_processors_experience,
            item=self.sweeps[0],
            test=True
        )
        task.run()
        not_working=0
        
        for p in all_presets:
            try :
                result=Result.objects.get(
                    item=self.sweeps[0],
                    preset=p
                )
            except :
                not_working+=1
                print(p.processor.pid)
                print(p.processor.get_processor().type)
        print(not_working, 'processors not working')
        """

    def test_all_processors_onebyone(self):
        all_processors=Processor.objects.all()
        for p in all_processors:
            preset=Preset.objects.create(processor=p)
            experience=Experience.objects.create()
            experience.presets.add(preset)
            task=Task.objects.create(
                experience=experience,
                item=self.item,
                test=True
            )
            task.run()
    
            result=Result.objects.get(
                    item=self.item,
                    preset=preset
                )
            self.assertTrue(result.has_file() or result.has_hdf5())    

            
class TestProcessorRequests(TimeSideTestServer):
    
    def test_processors_requests(self):
        #listProcessors
        response=self.client.get('/timeside/api/processors/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Processor.objects.count())

        #retrieveProcessor
        for p in response.data:
            get_processor=self.client.get(p['url'], format='json')
            self.assertEqual(get_processor.status_code,200)


class TestPresetRequests(TimeSideTestServer):


    def test_preset_requests(self):
        data={
            'processor': self.processor_url,
            'parameters':'{}'
        }

        preset=self.client.post('/timeside/api/presets/',data=data,format='json')
        self.assertEqual(preset.status_code, 201)

        #retrieve
        preset=self.client.get(preset.data['url'], format='json')
        self.assertEqual(preset.status_code, 200)

        #list_presets
        list_preset=self.client.get('/timeside/api/presets/',format='json')
        self.assertEqual(len(list_preset.data),Preset.objects.count())

        #update 
        data={
            'processor': self.processor2_url,
            'parameters':'{}'
        }
        preset=self.client.put(preset.data['url'],data)
        self.assertEqual(preset.status_code,200)
        self.assertEqual(preset.data['processor'][-38:],self.processor2_url[-38:])
        
        #delete preset
        self.delete_test(preset)

class TestExperienceRequests(TimeSideTestServer):

    def test_experience_requests(self):

        #create experience
        data_experience={
            'title':'test_experience_requests',
            'presets':[self.preset_url]
        }
        
        experience=self.client.post('/timeside/api/experiences/',data_experience,format='json')
        self.assertEqual(experience.status_code,201)

        #retrieve
        experience=self.client.get(experience.data['url'], format='json')
        self.assertEqual(experience.status_code, 200)
        
        #list experiences
        list_experiences=self.client.get('/timeside/api/experiences/',format='json')
        self.assertEqual(len(list_experiences.data),Experience.objects.count())
        
        #update
        data_experience={
            'title':'test_update',
            'presets':[self.preset2_url]
        }
        
        experience=self.client.put(experience.data['url'],data_experience)
        self.assertEqual(experience.status_code,200)
        self.assertEqual(experience.data['presets'][0][-40:],self.preset2_url[-40:])

        #delete
        self.delete_test(experience)

class TestTaskRequests(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.data_task={
            'experience':self.experience_url,
            'status': 2,
            'item':self.item_url,
            'test':True,
        }

    def test_task_requests(self):
        
        #createTask
        len_results=Result.objects.count()

        task=self.client.post('/timeside/api/tasks/',self.data_task)
        self.assertEqual(len_results+1, Result.objects.count())

        #retrieve
        task=self.client.get(task.data['url'], format='json')
        self.assertEqual(task.status_code, 200)
        
        #list tasks
        list_tasks=self.client.get('/timeside/api/tasks/')
        self.assertEqual(len(list_tasks.data),Task.objects.count())
        
        #update with new item
        self.data_task['item']=self.item2_url
        task=self.client.put(task.data['url'],self.data_task)
        self.assertEqual(task.status_code,200)
        self.assertEqual(len_results+2, Result.objects.count())

    def test_task_with_selection(self):
        len_results=Result.objects.count()

        #create with selection
        task=self.client.post('/timeside/api/tasks/',self.data_task)
        self.assertEqual(task.status_code, 201)
        self.assertEqual(len_results+1, Result.objects.count())
    

        #update change experience
        self.experience.presets.add(self.preset2)
        self.data_task['experience']=self.experience_url
        task=self.client.put(task.data['url'],self.data_task)
        self.assertEqual(task.status_code, 200)
        self.assertEqual(len_results+2, Result.objects.count())

        #delete
        self.delete_test(task)
        

    