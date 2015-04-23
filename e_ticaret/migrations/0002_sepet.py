# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('e_ticaret', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sepet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('musteri', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('urunler', models.ManyToManyField(to='e_ticaret.SepetUrunu')),
            ],
        ),
    ]
