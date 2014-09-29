# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subject',
            field=models.CharField(default=datetime.date(2014, 9, 17), max_length=256),
            preserve_default=False,
        ),
    ]
