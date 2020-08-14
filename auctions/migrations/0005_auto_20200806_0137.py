# Generated by Django 3.0.8 on 2020-08-06 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200805_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid_listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.Auction'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(),
        ),
    ]
