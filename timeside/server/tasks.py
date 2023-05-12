from __future__ import absolute_import

import time
import gc

from django.db import transaction

from celery import shared_task
from celery.result import AsyncResult
from celery.result import GroupResult

from .models import Item, Selection, Preset, Experience, Task, Provider
from .models import _DONE

from timeside.core.exceptions import ProviderError

from celery.utils.log import get_task_logger

from django.conf import settings

import redis
r = redis.Redis.from_url(settings.MESSAGE_BROKER)

logger = get_task_logger(__name__)


@shared_task
def task_run(task_id, test=False):
    # test : can't access the db with celery when testing
    task = Task.objects.get(uuid=task_id)
    results = []
    results_id = []

    if task.author:
        message = str(task.author.username) + ":" + str(task.uuid)
    else:
        message = str(task.uuid)

    r.publish(
        'timeside-task-start',
        message
    )
    if task.selection:
        logger.info(
            f'Apply {str(task.experience)} on {str(task.selection)} in task {str(task)}'
        )
        for item in task.selection.get_all_items():
            if test:
                results.append(
                    experience_run(
                        str(task.uuid),
                        str(task.experience.uuid),
                        str(item.uuid),
                    )
                )    
            else: 
                results.append(
                    experience_run.delay(
                        str(task.uuid),
                        str(task.experience.uuid),
                        str(item.uuid),
                    )
                )    
        if not test: 
            results_id = [res.id for res in results]

    elif task.item:
        logger.info(
            f'Apply {str(task.experience)} on {str(task.item)} in task {str(task)}'
        )
        if test: 
            results.append(
                experience_run(
                    str(task.uuid),
                    str(task.experience.uuid),
                    str(task.item.uuid),
                ),
            )
        else: 
            results.append(
                experience_run.delay(
                    str(task.uuid),
                    str(task.experience.uuid),
                    str(task.item.uuid),
                )
            )
            results_id = [res.id for res in results]
            print(results_id)

    elif not task.item:
        logger.info(
            f'Apply {str(task.experience)} with no item in task {str(task)}'
        )
        if test:
            results.append(
                experience_run(
                    str(task.uuid),
                    str(task.experience.uuid),
                    None,
                ),
            )
        else:
            results.append(
                experience_run.delay(
                    str(task.uuid),
                    str(task.experience.uuid),
                    None,
                )
            )
            results_id = [res.id for res in results]
            print(results_id)

    if test: 
        task_monitor(task_id, results_id)
    else: 
        task_monitor.delay(task_id, results_id)


@shared_task
def experience_run(task_id, exp_id, item_id):
    
    task = Task.objects.get(uuid=task_id)
    experience = Experience.objects.get(uuid=exp_id)
    if item_id:
        item = Item.objects.get(uuid=item_id)
    else:
        item = None

    if task.author:
        author = task.author.username
    else:
        author = ''

    try:
        logger.info(f'Run {str(experience)} on {str(item)}')
        if item and not (item.source_url or item.source_file):
            logger.info(f'Item does not have any source_file nor source_url. \
                            Saving it again to retrieve data. \
                            Please re-run task {str(task.uuid)} after finish')
            item.save()
        else:
            r.publish(
                'timeside-experience-start',

                str(author) +
                ":" + str(task.uuid) +
                ":" + str(experience.uuid) +
                ":" + str(item)
            )
            experience.run(task=task, item=item)
            gc.collect()
            r.publish(
                'timeside-experience-done',
                str(author) +
                ":" + str(task.uuid) +
                ":" + str(experience.uuid) +
                ":" + str(item)
            )
    except Exception as e:
        r.publish(
            'timeside-experience-fail',
            str(author) +
            ":" + str(task.uuid) +
            ":" + str(experience.uuid) +
            ":" + str(item)
        )
        raise e


@shared_task
def task_monitor(task_id, results_id):
    results = [AsyncResult(id) for id in results_id]
    task = Task.objects.get(uuid=task_id)
    logger.info(f'Wait for results of {str(task)} to be ready')
    while not all([res.ready() for res in results]):
        time.sleep(1)
    logger.info(f'{str(task)} is done')
    task.status_setter(_DONE)


@shared_task
def item_post_save_async(uuid, download=True, waveform=False):
    items = Item.objects.filter(uuid=uuid)
    # arbitrary sleep ensuring the item.save() is already done
    while not items:
        items = Item.objects.filter(uuid=uuid)
        time.sleep(0.5)
    items.update(lock=True)
    item = items[0]

    if not item.source_file:
        source_file = ""
        if item.external_id or item.external_uri:
            title, source_file = item.get_resource(download=download)
        items.update(source_file=source_file.replace(settings.MEDIA_ROOT, ''))
        items.update(title=title)
        item = Item.objects.get(uuid=uuid)

    if item.source_file:
        sha1 = item.get_hash()
        mime_type = item.get_mime_type()
        audio_duration = item.get_audio_duration()
        samplerate = item.get_audio_samplerate()
        items.update(
            sha1=sha1,
            mime_type=mime_type,
            audio_duration=audio_duration,
            samplerate=samplerate,
            )
        if waveform:
            item.process_waveform()

    items.update(lock=False)


@shared_task
def item_post_save_async2(uuid, download=True, waveform=False):
    items = Item.objects.filter(uuid=uuid)
    item = items[0]

    if not item.source_file:
        if item.external_id or item.external_uri:
            title, source_file = item.get_resource(download=download)
            items.update(title=title, source_file=source_file)

    if item.source_file:
        sha1 = item.get_hash()
        mime_type = item.get_mime_type()
        audio_duration = item.get_audio_duration()
        samplerate = item.get_audio_samplerate()
        items.update(
            sha1=sha1,
            mime_type=mime_type,
            audio_duration=audio_duration,
            samplerate=samplerate,
            )

        if waveform:
            item.process_waveform()


@shared_task
def item_post_save_async3(uuid, download=True, waveform=True):
    item = Item.objects.get(uuid=uuid)
    title = ""

    if not item.source_file and (item.external_id or item.external_uri):
        title, source_file = item.get_resource(download=download)
        item.source_file = source_file.replace(settings.MEDIA_ROOT, '')
        item.title = title
        item.save_without_signals()

    if item.source_file:
        item.sha1 = item.get_hash()
        item.mime_type = item.get_mime_type()
        item.audio_duration = item.get_audio_duration()
        item.samplerate = item.get_audio_samplerate()
        if waveform:
            item.process_waveform()
        item.save_without_signals()


