# Generated by Django 3.0.8 on 2020-08-08 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200808_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='current_bid',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
