# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-31 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0003_auto_20180830_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diskinfo',
            name='disk_disk_time',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=250, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]
