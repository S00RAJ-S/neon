# Generated by Django 4.0.4 on 2022-11-10 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neonuser', '0016_neonlogin_twofa_alter_orders_orderedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='neonlogin',
            name='twofakey',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orderedtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 10, 15, 59, 49, 927764)),
        ),
    ]