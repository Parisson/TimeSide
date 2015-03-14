from __future__ import absolute_import

from celery import shared_task
from .models import Task


@shared_task
def task_run(id):
    task = Task.objects.get(id=id)
    task.run()


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)