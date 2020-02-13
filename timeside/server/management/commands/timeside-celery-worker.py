import shlex
import subprocess

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import autoreload

# thanks to https://medium.com/aubergine-solutions/auto-reload-development-mode-for-celery-worker-using-docker-compose-and-django-management-2ba8e313eb37


def restart_celery(*args, **kwargs):
    kwargs = kwargs['kwargs']
    kill_worker_cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(kill_worker_cmd))
    start_worker_cmd = 'celery -A worker worker --loglevel=%s --logfile=%s' % (kwargs['loglevel'], kwargs['logfile'])
    subprocess.call(shlex.split(start_worker_cmd))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-lf', '--logfile',
            dest='logfile',
            help='define the logfile')

        parser.add_argument('-ll', '--loglevel',
            dest='loglevel',
            help='define the loglevel')

    def handle(self, *args, **options):
        self.stdout.write('Starting celery worker with autoreload...')
        kwargs = {
                'loglevel': options.get('loglevel'),
                'logfile': options.get('logfile')
            }
        autoreload.run_with_reloader(restart_celery, args=None, kwargs=kwargs)