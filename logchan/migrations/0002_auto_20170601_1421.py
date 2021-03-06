# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-01 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logchan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='id',
        ),
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.CharField(default='board', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
