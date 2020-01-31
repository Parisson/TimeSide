
import os, sys
import logging

from celery import Celery
from celery.signals import after_setup_task_logger
from celery.app.log import TaskFormatter

from django.conf import settings

sys.path.append(os.path.dirname('.'))
sys.path.append(os.path.dirname('..'))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('app')

# logger
logger = logging.getLogger(__name__)

@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    # FileHandler
    fh = logging.FileHandler('/var/log/celery/worker.log')
    fh.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(('Request: {0!r}'.format(self.request)))