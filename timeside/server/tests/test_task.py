from timeside.server.tests.timeside_test_server import TimeSideTestServer
from rest_framework.reverse import reverse
from timeside.server.models import *
import h5py


class TestTask(TimeSideTestServer):

    def test_simple_task(self):
        sweep_32000=Item.objects.get(title="sweep_32000")
        pitch_processor=Processor.objects.get(pid="aubio_pitch")
        pitch_preset=Preset.objects.get(processor=pitch_processor)
        pitch_experience=Experience.objects.create(
            title='pitch for unittest'
        )
        pitch_experience.presets.add(pitch_preset)
        task=Task.objects.create(
            experience=pitch_experience,
            item=sweep_32000,
            test=True
        )
        task.run()
        result=Result.objects.get(
            preset=pitch_preset,
            item=sweep_32000
        )
        print([e.title for e in Experience.objects.all()])


    def test_all_processors(self):
        all_processors=Processor.objects.all()
        all_presets=[]
        for p in all_processors:
            all_presets.append(Preset.objects.create(processor=p))
            if p.pid=="waveform_analyzer":
                waveform_processor=p
        
        #waveform_processor=Processor.objects.get(pid="waveform_analyzer")
        all_presets=[Preset.objects.create(processor=waveform_processor)]

        all_processors_experience=Experience.objects.create()
        all_processors_experience.presets.set(all_presets)
        sweep_selection=Selection.objects.create()
        #add sweep.ogg, sweep.flac, sweep.mp3 and sweep.wav
        all_sweep=[Item.objects.filter(title='sweep')]
        all_sweep=[Item.objects.get(title="sweep_32000")]
        sweep_selection.items.set(all_sweep)
        task=Task.objects.create(
            experience=all_processors_experience,
            selection=sweep_selection,
            test=True
        )
        task.run()
        not_working=0
        
        for p in range(len(all_presets)):

            try :
                result=Result.objects.get(
                    item=all_sweep[0],
                    preset=all_presets[p]
                )
            except :
                not_working+=1
                print(all_presets[p].processor.pid)
        print(not_working, 'processors not working')




