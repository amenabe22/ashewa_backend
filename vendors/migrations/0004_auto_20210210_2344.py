# Generated by Django 3.1.2 on 2021-02-10 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_order_total_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_quantity',
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.BigIntegerField(null=True),
        ),
    ]