# Generated by Django 3.1.2 on 2021-02-11 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_ecommerce', '0002_auto_20210207_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='product_brand',
        ),
    ]