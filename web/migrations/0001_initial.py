# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-03 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sn', models.CharField(max_length=250)),
                ('sn_1', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('name1', models.CharField(max_length=250)),
                ('family', models.CharField(max_length=250)),
                ('status', models.CharField(max_length=550)),
                ('time', models.DateTimeField()),
                ('boot_time', models.CharField(max_length=250)),
                ('cpu', models.CharField(max_length=250)),
                ('memory', models.CharField(max_length=250)),
                ('disk', models.CharField(max_length=550)),
                ('raid', models.CharField(max_length=550)),
                ('network', models.CharField(max_length=550)),
                ('mac', models.CharField(max_length=550)),
                ('mac_addr', models.CharField(max_length=550)),
                ('ip', models.CharField(blank=True, max_length=550)),
                ('bios', models.CharField(max_length=250)),
                ('bmc', models.CharField(max_length=250)),
                ('sel', models.TextField()),
                ('stress_test', models.CharField(max_length=250)),
                ('hostname', models.CharField(max_length=250)),
                ('disk_num', models.IntegerField()),
                ('message', models.TextField()),
                ('fru', models.TextField()),
                ('smart_info', models.TextField(blank=True)),
                ('enclosure', models.FileField(blank=True, upload_to=b'', verbose_name='breakin')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668\u4fe1\u606f',
                'verbose_name_plural': '\u8001\u5316\u6d4b\u8bd5\u7cfb\u7edf',
            },
        ),
    ]
