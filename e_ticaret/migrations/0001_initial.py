# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('yonetim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MusteriProfili',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('adresi', models.TextField()),
                ('cep_telefonu', models.CharField(max_length=10, verbose_name=b'Cep Telefonu', blank=True)),
                ('ev_telefonu', models.CharField(max_length=10, verbose_name=b'Ev Telefonu', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SepetUrunu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('miktar', models.PositiveIntegerField()),
                ('urun', models.ForeignKey(to='yonetim.Urun')),
            ],
        ),
    ]
