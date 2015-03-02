# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import accounts.services


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('accounts', '0004_auto_20150227_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='activation_key',
            field=models.CharField(default=accounts.services.make_activation_key, max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(related_query_name=b'user', related_name='user_set', to='auth.Group', blank=True, help_text=b'The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name=b'groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text=b'Designates that this user has all permissions without explicitly assigning them.', verbose_name=b'superuser status'),
            preserve_default=True,
        ),
    ]
