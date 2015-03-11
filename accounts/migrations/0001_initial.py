# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import accounts.services


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('role', models.CharField(max_length=255)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('is_superuser', models.BooleanField(default=False, help_text=b'Designates that this user has all permissions without explicitly assigning them.', verbose_name=b'superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('activation_key', models.CharField(default=accounts.services.make_activation_key, max_length=40)),
                ('groups', models.ManyToManyField(related_query_name=b'user', related_name='user_set', to='auth.Group', blank=True, help_text=b'The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name=b'groups')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
