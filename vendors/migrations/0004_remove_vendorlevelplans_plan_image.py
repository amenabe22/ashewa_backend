# Generated by Django 3.1.2 on 2020-12-05 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_vendorlevelplans_purchase_bonus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendorlevelplans',
            name='plan_image',
        ),
    ]
