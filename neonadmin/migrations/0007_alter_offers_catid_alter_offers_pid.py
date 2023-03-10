# Generated by Django 4.0.4 on 2022-10-31 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neonadmin', '0006_alter_offers_catid_alter_offers_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='catid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neonadmin.categories', unique=True),
        ),
        migrations.AlterField(
            model_name='offers',
            name='pid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neonadmin.products', unique=True),
        ),
    ]
