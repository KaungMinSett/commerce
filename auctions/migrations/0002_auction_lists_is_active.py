# Generated by Django 5.0.1 on 2024-04-20 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_lists',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]