# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0003_auto_20150412_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='EOD',
            field=models.TimeField(default=b'17:00:00'),
        ),
        migrations.AddField(
            model_name='account',
            name='nickname',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
