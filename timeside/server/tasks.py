from __future__ import absolute_import

from celery import shared_task
from .models import Item, Selection, Preset, Experience, Task


@shared_task
def task_run(id):
    task = Task.objects.get(id=id)
    task.run()

@shared_task
def experience_run(exp_id, item_id):
    item = Item.objects.get(id=item_id)
    experience = Experience.objects.get(id=exp_id)
    item.run(experience)
