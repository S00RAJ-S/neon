# Generated by Django 4.0.4 on 2022-10-26 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neonuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 26, 17, 58, 10, 68257)),
        ),
    ]
