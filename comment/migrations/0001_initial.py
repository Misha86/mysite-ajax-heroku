# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-13 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('comments_text', models.TextField(max_length=200, verbose_name='Текст коментаря')),
                ('comments_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Article', verbose_name='Коментар для статті')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
                'db_table': 'comments',
            },
        ),
    ]
