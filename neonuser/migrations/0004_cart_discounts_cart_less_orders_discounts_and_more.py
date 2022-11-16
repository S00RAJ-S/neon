# Generated by Django 4.0.4 on 2022-10-27 08:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neonadmin', '0002_coupens'),
        ('neonuser', '0003_alter_orders_orderedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discounts',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='neonadmin.coupens'),
        ),
        migrations.AddField(
            model_name='cart',
            name='less',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='discounts',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='neonadmin.coupens'),
        ),
        migrations.AddField(
            model_name='orders',
            name='less',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 43, 40, 839086)),
        ),
    ]
