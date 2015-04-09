# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acct_num', models.IntegerField()),
                ('acct_name', models.CharField(max_length=100)),
                ('acct_server', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(verbose_name=b'dbtime')),
                ('equity_open', models.DecimalField(max_digits=10, decimal_places=2)),
                ('equity_close', models.DecimalField(max_digits=10, decimal_places=2)),
                ('equity_low', models.DecimalField(max_digits=10, decimal_places=2)),
                ('equity_high', models.DecimalField(max_digits=10, decimal_places=2)),
                ('acct_id', models.ForeignKey(to='Trading.Account')),
            ],
        ),
    ]
