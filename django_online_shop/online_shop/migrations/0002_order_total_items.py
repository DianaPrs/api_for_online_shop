# Generated by Django 3.1.3 on 2021-01-30 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_items',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
