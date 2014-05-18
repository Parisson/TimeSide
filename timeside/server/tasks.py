
from __future__ import absolute_import

from timeside.server.celery import app


@app.task
def process(pipe):
    pipe.run()
