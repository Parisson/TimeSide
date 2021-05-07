from __future__ import absolute_import

import time
import gc

from celery import shared_task
from celery.result import AsyncResult
from celery.result import GroupResult

from .models import Item, Selection, Preset, Experience, Task
from .models import _DONE

from celery.task import chord
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def task_run(task_id,test=False):
    #test : can't access the db with celery when testing
    task = Task.objects.get(uuid=task_id)
    results = []
    results_id=[]
    if task.selection:
        logger.info(f'Apply {str(task.experience)} on {str(task.selection)} in task {str(task)}')
        for item in task.selection.get_all_items():
            if test :
                results.append(experience_run(str(task.experience.uuid), str(item.uuid)))    
            else : 
                results.append(experience_run.delay(str(task.experience.uuid), str(item.uuid)))    
        if not test : 
            results_id = [res.id for res in results]
    elif task.item:
        logger.info(f'Apply {str(task.experience)} on {str(task.item)} in task {str(task)}')
        if test : 
            results.append(experience_run(str(task.experience.uuid), str(task.item.uuid)))
        else : 
            results.append(experience_run.delay(str(task.experience.uuid), str(task.item.uuid)))
            results_id = [res.id for res in results]
    if test : 
        task_monitor(task_id, results_id)
    else : 
        task_monitor.delay(task_id, results_id)


@shared_task
def experience_run(exp_id, item_id):
    item = Item.objects.get(uuid=item_id)
    experience = Experience.objects.get(uuid=exp_id)
    logger.info(f'Run {str(experience)} on {str(item)}')
    item.run(experience)
    gc.collect()

@shared_task
def task_monitor(task_id, results_id):
    results = [AsyncResult(id) for id in results_id]
    task = Task.objects.get(uuid=task_id)
    logger.info(f'Wait for results of {str(task)} to be ready')
    while not all([res.ready() for res in results]):
        time.sleep(1)
    logger.info(f'{str(task)} is done')
    task.status_setter(_DONE)
