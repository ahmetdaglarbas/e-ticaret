# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yonetim.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resim', models.ImageField(upload_to=yonetim.models.upload_to, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reyon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adi', models.CharField(max_length=50, verbose_name=b'Ad\xc4\xb1')),
                ('aciklama', models.CharField(max_length=50, verbose_name=b'A\xc3\xa7\xc4\xb1klama', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Urun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adi', models.CharField(max_length=50, verbose_name=b'Ad\xc4\xb1')),
                ('aciklama', models.CharField(max_length=50, verbose_name=b'A\xc3\xa7\xc4\xb1klama', blank=True)),
                ('fiyati', models.FloatField(verbose_name=b'Fiyat\xc4\xb1')),
                ('vitrin', models.BooleanField(verbose_name=b'Vitrin \xc3\x9cr\xc3\xbcn\xc3\xbc')),
                ('reyon', models.ForeignKey(verbose_name=b'Reyon', to='yonetim.Reyon')),
            ],
            options={
                'ordering': ['adi'],
            },
        ),
        migrations.AddField(
            model_name='resim',
            name='urun',
            field=models.ForeignKey(to='yonetim.Urun'),
        ),
    ]
