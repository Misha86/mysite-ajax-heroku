# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-22 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата народження'),
        ),
    ]
