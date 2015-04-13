# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0002_equity_open_lots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equity',
            name='equity_close',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='equity',
            name='equity_high',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='equity',
            name='equity_low',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='equity',
            name='equity_open',
            field=models.IntegerField(),
        ),
    ]
