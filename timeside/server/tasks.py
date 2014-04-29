
from __future__ import absolute_import

from timeside.webserver.celery import app

@app.task
def process(pipe):
    pipe.run()
