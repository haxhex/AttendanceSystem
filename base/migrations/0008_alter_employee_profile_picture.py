# Generated by Django 4.1.3 on 2022-12-17 02:10

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_employee_department_employee_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile.png', null=True, upload_to=base.models.mentor_photos),
        ),
    ]
