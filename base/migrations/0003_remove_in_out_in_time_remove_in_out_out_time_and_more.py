# Generated by Django 4.1.3 on 2022-11-26 05:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='in_out',
            name='in_time',
        ),
        migrations.RemoveField(
            model_name='in_out',
            name='out_time',
        ),
        migrations.AddField(
            model_name='in_out',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='in_out',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]