# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('things', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'image_profile', blank=True)),
                ('automaticcontrollers', models.ManyToManyField(to='things.AutomaticController', null=True, blank=True)),
                ('cameras', models.ManyToManyField(to='cameras.Camera', null=True, blank=True)),
                ('things', models.ManyToManyField(to='things.Thing', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
