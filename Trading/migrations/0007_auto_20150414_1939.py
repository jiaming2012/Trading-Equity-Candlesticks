# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0006_auto_20150413_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equity',
            name='open_lots',
            field=models.FloatField(),
        ),
    ]
