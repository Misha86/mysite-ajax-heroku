# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-31 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
        ('loginsys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comments_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='loginsys.Profile', verbose_name='Автор коментаря'),
        ),
    ]