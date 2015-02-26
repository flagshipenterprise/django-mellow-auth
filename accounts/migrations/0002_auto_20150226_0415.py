# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='parent',
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]
