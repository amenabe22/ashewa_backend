# Generated by Django 3.1.2 on 2021-03-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_ecommerce', '0004_paymenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttype',
            name='core_transaction_outlet',
            field=models.CharField(blank=True, choices=[('cash', 'Cash'), ('bank', 'Bank Payment')], max_length=4, null=True),
        ),
    ]
