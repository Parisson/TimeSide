from __future__ import absolute_import

import time
import gc

from celery import shared_task
from celery.result import AsyncResult
from celery.result import GroupResult

from .models import Item, Selection, Preset, Experience, Task
from .models import _DONE

from celery.task import chord


@shared_task
def task_run(task_id):
    task = Task.objects.get(uuid=task_id)
    results = []
    if task.selection:
        for item in task.selection.get_all_items():
            results.append(experience_run.delay(str(task.experience.uuid), str(item.uuid)))
        results_id = [res.id for res in results]
    elif task.item:
        results.append(experience_run.delay(str(task.experience.uuid), str(task.item.uuid)))
        results_id = [res.id for res in results]
    task_monitor.delay(task_id, results_id)


@shared_task
def experience_run(exp_id, item_id):
    item = Item.objects.get(uuid=item_id)
    experience = Experience.objects.get(uuid=exp_id)
    item.run(experience)
    gc.collect()

@shared_task
def task_monitor(task_id, results_id):
    results = [AsyncResult(id) for id in results_id]

    while not all([res.ready() for res in results]):
        time.sleep(1)

    task = Task.objects.get(uuid=task_id)
    task.status_setter(_DONE)
