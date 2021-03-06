# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_api', '0003_auto_20170902_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='result',
            field=models.CharField(blank=True, choices=[(('WHITE',), 'WWHITE'), (('BLACK',), 'BLACK'), (('DRAW',), 'DRAW'), ('Undetermined', 'Undetermined')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournament_api.Tournament'),
        ),
    ]
