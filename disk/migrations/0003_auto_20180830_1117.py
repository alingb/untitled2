# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-30 03:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('disk', '0002_auto_20180830_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemanger',
            name='file_time',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]