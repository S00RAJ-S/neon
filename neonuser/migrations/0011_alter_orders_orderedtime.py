# Generated by Django 4.0.4 on 2022-10-29 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neonuser', '0010_remove_orders_finalamt_cart_finalamt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 29, 12, 57, 26, 807628)),
        ),
    ]