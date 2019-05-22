# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeside_server', '0022_auto_20190506_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='external_id',
            field=models.CharField(max_length=256, verbose_name='external_id', blank=True),
        ),
    ]
