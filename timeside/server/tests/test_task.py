from timeside.server.models import *
from timeside.server.tests.timeside_test_server import TimeSideTestServer


class TestTask(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')
        self.sweeps=Item.objects.filter(title='sweep')


    def test_simple_task(self):
        sweep0=self.sweeps[0]
        pitch_processor=Processor.objects.get(pid="aubio_pitch")
        pitch_preset=Preset.objects.get(processor=pitch_processor)
        pitch_experience=Experience.objects.create(
            title='pitch for unittest'
        )
        pitch_experience.presets.add(pitch_preset)
        task=Task.objects.create(
            experience=pitch_experience,
            item=sweep0,
            test=True
        )
        task.run()
        result=Result.objects.get(
            preset=pitch_preset,
            item=sweep0
        )


    def test_all_processors(self):
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

    def test_all_processors_onebyone(self):
        sweep0=self.sweeps[0]
        all_processors=Processor.objects.all()
        for p in all_processors:
            preset=Preset.objects.create(processor=p)
            experience=Experience.objects.create()
            experience.presets.add(preset)
            task=Task.objects.create(
                experience=experience,
                item=sweep0,
                test=True
            )
            task.run()
            try :
                result=Result.objects.get(
                        item=sweep0,
                        preset=preset
                    )
            except:
                print(preset.processor.pid)

    def test_experience_all(self):
        sweep0=self.sweeps[0]
        experience_all=Experience.objects.get(title='All')
        task=Task.objects.create(
                experience=experience_all,
                item=sweep0,
                test=True
            )
        task.run()
        print(experience_all.presets)
        for p in list(experience_all.presets):
            try :
                result=Result.objects.get(
                        item=sweep0,
                        preset=p
                    )
            except:
                print(p.processor.pid)


class TestTaskWithRequests(TimeSideTestServer):

    def setUp(self):
        TimeSideTestServer.setUp(self)
        self.client.login(username='admin', password='admin')


    def test_processors_requests(self):
        #listProcessors
        response=self.client.get('/timeside/api/processors/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Processor.objects.count())

        #retrieveProcessor
        for p in response.data:
            get_processor=self.client.get(p['url'], format='json')
            self.assertEqual(get_processor.status_code,200)


    def update_test(self,obj,data):
        put_request=self.client.put(obj.data['url'],data,format='json')
        for key in data.keys():
            self.assertEqual(put_request.data[key],data[key])

    def delete_test(self,obj):
        delete_request=self.client.delete(obj.data['url'],format='json')
        self.assertEqual(delete_request.status_code,204)
        get_request=self.client.get(obj.data['url'],format='json')
        self.assertEqual(get_request.status_code,404)

    def test_preset_requests(self):
        list_processor=self.client.get('/timeside/api/processors/', format='json')
        data={
            'processor': list_processor.data[0]['url'],
        }

        preset=self.client.post('/timeside/api/presets/',data=data,format='json')
        self.assertEqual(preset.status_code, 201)
        
        #TODO : do not create a new preset when parameters are the same
        #preset2=self.client.post('/timeside/api/presets/',data=data,format='json')
        #self.assertEqual(preset.data,preset2.data)

        #retrieve
        preset=self.client.get(preset.data['url'], format='json')
        self.assertEqual(preset.status_code, 200)

        #list_presets
        list_preset=self.client.get('/timeside/api/presets/',format='json')
        self.assertEqual(len(list_preset.data),Preset.objects.count())

        #update 
        data={
            'processor': list_processor.data[1]['url'],
            'parameters':'testing update'
        }
        self.update_test(preset,data)

        #partial update
        #TODO
        
        #delete preset
        self.delete_test(preset)

    

    def test_experience_requests(self):
        #create presets for experience
        list_processor=self.client.get('/timeside/api/processors/', format='json')
        data_preset1={
            'processor': list_processor.data[0]['url'],
        }
        data_preset2={
            'processor': list_processor.data[1]['url'],
        }
        preset1=self.client.post('/timeside/api/presets/',data_preset1,format='json')
        preset2=self.client.post('/timeside/api/presets/',data_preset2,format='json')

        #create experience
        data_experience={
            'title':'test_experience_requests',
            'presets':[preset1.data['url'],preset2.data['url']]
        }
        
        experience=self.client.post('/timeside/api/experiences/',data_experience,format='json')
        self.assertEqual(experience.status_code,201)

        #TODO : not create a new experience when parameters are the same
        #experience2=self.client.post('/timeside/api/experiences/',data=data_experience,format='json')
        #self.assertEqual(experience.data,experience2.data)

        #retrieve
        experience=self.client.get(experience.data['url'], format='json')
        self.assertEqual(experience.status_code, 200)
        
        #list experiences
        list_experiences=self.client.get('/timeside/api/experiences/',format='json')
        self.assertEqual(len(list_experiences.data),Experience.objects.count())
        
        #update
        data_experience={
            'title':'test_experience_update',
            'presets':[preset1.data['url']]
        }
        self.update_test(experience,data_experience)

        #partial update
        #TODO

        #delete
        self.delete_test(experience)

    def test_task_requests(self):
        #create experience for task
        preset=Preset.objects.create(processor=Processor.objects.get(pid='aubio_pitch'))
        experience_obj=Experience.objects.create()
        experience_obj.presets.add(preset)
        experience=self.client.get('/timeside/api/experiences/'+str(experience_obj.uuid)+'/')
        self.assertEqual(experience.status_code,200)

        #get item0
        list_items=self.client.get('/timeside/api/items/')
        self.assertEqual(list_items.status_code,200)
        item=list_items.data[0]

        #createTask
        len_results=Result.objects.count()

        data_task={
            'experience':experience.data['url'],
            'status': 2,
            'item':item['url'],
            'test':True,
        }
        task=self.client.post('/timeside/api/tasks/',data_task)
        self.assertEqual(len_results+1, Result.objects.count())
        #TODO : not create a new task when parameters are the same

        #retrieve
        task=self.client.get(task.data['url'], format='json')
        self.assertEqual(task.status_code, 200)
        
        #list experiences
        list_tasks=self.client.get('/timeside/api/tasks/')
        self.assertEqual(len(list_tasks.data),Task.objects.count())
        
        #update with new item
        item=list_items.data[1]
        data_task['item']=item['url']
        task=self.client.put(task.data['url'],data_task)
        self.assertEqual(task.status_code,200)
        self.assertEqual(len_results+2, Result.objects.count())

        #update item to selection
        #create a selection with item 2 and 3
        item2=list_items.data[2]
        item3=list_items.data[3]
        data_selection={
            'items':[item2['url'],item3['url']]
        }

        selection=self.client.post('/timeside/api/selections/',data_selection)
        self.assertEqual(selection.status_code,201)

        #update with this new selection
        data_task['selection']=selection.data['url']
        task=self.client.put(task.data['url'],data_task)
        self.assertEqual(task.status_code, 200)
        self.assertEqual(len_results+4, Result.objects.count())

        #update change experience
        preset=Preset.objects.create(processor=Processor.objects.get(pid='aubio_silence'))
        experience_obj=Experience.objects.create()
        experience_obj.presets.add(preset)
        experience=self.client.get('/timeside/api/experiences/'+str(experience_obj.uuid)+'/')
        self.assertEqual(experience.status_code,200)

        data_task['experience']=experience.data['url']
        task=self.client.put(task.data['url'],data_task)
        self.assertEqual(task.status_code, 200)
        self.assertEqual(len_results+6, Result.objects.count())

        #partial update
        #TODO
        
        #delete
        self.delete_test(task)
        

    