# Generated by Django 3.0.8 on 2020-08-08 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200807_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='auction_winner',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='img_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]