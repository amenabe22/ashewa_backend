# Generated by Django 3.1.2 on 2021-02-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_ecommerce', '0003_remove_products_product_brand'),
        ('vendors', '0004_auto_20210210_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(blank=True, to='core_ecommerce.Products'),
        ),
    ]
