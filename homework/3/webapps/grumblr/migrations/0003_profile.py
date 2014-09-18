# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0002_post_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=256)),
                ('age', models.CharField(max_length=3)),
                ('motto', models.CharField(max_length=256)),
                ('fullname', models.CharField(max_length=128)),
                ('company', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
