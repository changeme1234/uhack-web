# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-02 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20171202_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='balance',
            field=models.FloatField(blank=True, default=1000.0, null=True),
        ),
    ]
