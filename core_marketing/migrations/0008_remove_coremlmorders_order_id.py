# Generated by Django 3.1.2 on 2021-02-10 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_marketing', '0007_auto_20210210_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coremlmorders',
            name='order_id',
        ),
    ]