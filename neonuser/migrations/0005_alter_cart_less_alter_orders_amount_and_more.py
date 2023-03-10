# Generated by Django 4.0.4 on 2022-10-27 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neonuser', '0004_cart_discounts_cart_less_orders_discounts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='less',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='less',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 14, 20, 20, 761521)),
        ),
    ]
