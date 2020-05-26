from django.conf import settings
from django.core.management.base import BaseCommand

import simplejson as json

from timeside.server.models import Analysis, SubProcessor, Processor, Preset


class Command(BaseCommand):
    help = """
    Clean disposable Analysis and SubProcessor for WASABI project
    leaving only:
    - spectrogram (grapher)
    - aubio_pitch(analyzer)
    - onset_detection(analyzer)
    """

    def subprocessor_cleanup(self):
        for subprocessor in SubProcessor.objects.all():
            subprocessor.delete()

    def analysis_cleanup(self):
        for analysis in Analysis.objects.all():
            analysis.delete()

    def handle(self, *args, **options):
        # delete sub processors and analysis
        self.subprocessor_cleanup()
        self.analysis_cleanup()

        # get processors
        proc_spectrogram, c = Processor.get_first_or_create(pid='spectrogram')
        proc_aubio_pitch, c = Processor.get_first_or_create(pid='aubio_pitch')
        proc_onset_detection, c = Processor.get_first_or_create(
            pid='onset_detection_function'
            )

        # get presets
        spectrogram, c = Preset.get_first_or_create(
            processor=proc_spectrogram,
            parameters='{}'
            )
        aubio_pitch, c = Preset.get_first_or_create(
            processor=proc_aubio_pitch,
            parameters=json.dumps(proc_aubio_pitch.get_parameters_default())
            )
        onset_detection, c = Preset.get_first_or_create(
            processor=proc_onset_detection,
            parameters=json.dumps(
                proc_onset_detection.get_parameters_default()
                )
            )

        # create Subprocessor
        sub_spectro, c = SubProcessor.objects.get_or_create(
            sub_processor_id='spectrogram',
            processor=proc_spectrogram
            )
        sub_pitch, c = SubProcessor.objects.get_or_create(
            sub_processor_id='aubio_pitch.pitch',
            processor=proc_aubio_pitch
            )
        sub_onset, c = SubProcessor.objects.get_or_create(
            sub_processor_id='onset_detection_function',
            processor=proc_onset_detection
            )

        # create Analysis
        Analysis.objects.get_or_create(
            sub_processor=sub_spectro,
            preset=spectrogram,
            title='Linear Spectrogram'
            )
        Analysis.objects.get_or_create(
            sub_processor=sub_pitch,
            preset=aubio_pitch,
            title='Pitch'
            )
        Analysis.objects.get_or_create(
            sub_processor=sub_onset,
            preset=onset_detection,
            title='Onset Detection'
            )
