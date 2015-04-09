# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trading', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equity',
            name='open_lots',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
            preserve_default=False,
        ),
    ]
