# Generated by Django 5.0.1 on 2024-04-18 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_auction_lists_bids_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_lists',
            name='Category',
            field=models.ManyToManyField(blank=True, null=True, related_name='auctions', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auction_lists',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
