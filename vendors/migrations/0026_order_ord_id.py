# Generated by Django 3.1.2 on 2021-03-07 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0025_order_sponsor'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ord_id',
            field=models.CharField(default='2246', max_length=10),
        ),
    ]
