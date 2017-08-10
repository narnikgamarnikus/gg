# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-09 14:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20170809_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 9, 14, 12, 45, 218920, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='services.ServiceUser'),
        ),
    ]