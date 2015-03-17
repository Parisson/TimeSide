from __future__ import absolute_import

from celery import shared_task
from .models import Item, Selection, Preset, Task


@shared_task
def task_run(id):
    task = Task.objects.get(id=id)
    task.run()


@shared_task
def experience_run(experience_id, item_id):
    item = Item.objects.get(id=item_id)
    experience = Experience.objects.get(id=experience_id)
    experience.run(item)


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)