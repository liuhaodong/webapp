# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_picture',
            field=models.ImageField(default=datetime.date(2014, 9, 30), upload_to=b'grumblr-id-photos', blank=True),
            preserve_default=False,
        ),
    ]
