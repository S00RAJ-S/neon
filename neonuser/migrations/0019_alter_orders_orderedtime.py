# Generated by Django 4.0.4 on 2022-11-11 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('neonuser', '0018_alter_orders_orderedtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 11, 9, 13, 59, 404431, tzinfo=utc)),
        ),
    ]
