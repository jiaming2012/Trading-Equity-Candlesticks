# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0005_account_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='EOD',
            field=models.TimeField(default=b'21:00:00'),
        ),
    ]
