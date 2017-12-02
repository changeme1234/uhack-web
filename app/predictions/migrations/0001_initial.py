# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-02 09:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('symbol', models.CharField(default='', max_length=10)),
                ('choice', models.CharField(choices=[('Up', 'Up'), ('Down', 'Down')], default='Up', max_length=4)),
                ('prediction_date', models.DateField()),
                ('done', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
