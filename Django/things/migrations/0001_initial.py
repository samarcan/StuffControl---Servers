# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticController',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_range', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=100)),
                ('value_range', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=100)),
                ('value_range', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('key', models.CharField(default=b'bM6GjAv6XVhfUVV', max_length=100)),
                ('controllers', models.ManyToManyField(to='things.Controller', null=True, blank=True)),
                ('sensors', models.ManyToManyField(to='things.Sensor', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='log_sensor',
            field=models.ManyToManyField(to='things.Value', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='controller',
            name='log_control',
            field=models.ManyToManyField(to='things.Value', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='automaticcontroller',
            name='controller',
            field=models.ForeignKey(to='things.Controller'),
        ),
        migrations.AddField(
            model_name='automaticcontroller',
            name='controllerthing',
            field=models.ForeignKey(related_name='controller_things_automaticcontroller_related', to='things.Thing'),
        ),
        migrations.AddField(
            model_name='automaticcontroller',
            name='sensor',
            field=models.ForeignKey(to='things.Sensor'),
        ),
        migrations.AddField(
            model_name='automaticcontroller',
            name='sensorthing',
            field=models.ForeignKey(related_name='sensor_things_automaticcontroller_related', to='things.Thing'),
        ),
    ]
