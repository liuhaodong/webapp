# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_profile_id_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id_picture',
            field=models.ImageField(upload_to=b'grumblr_id_photos', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
