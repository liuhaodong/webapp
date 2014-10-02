# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0008_blockuser_dislikegrumbl'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
