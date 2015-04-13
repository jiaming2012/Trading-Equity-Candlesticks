# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0004_auto_20150413_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='Start',
            field=models.TimeField(default=b'17:00:00'),
        ),
    ]
