# Generated by Django 3.1.2 on 2021-02-14 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_vendorlevelplans_created_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendorlevelplans',
            old_name='created_timestamp',
            new_name='timestamp',
        ),
    ]
