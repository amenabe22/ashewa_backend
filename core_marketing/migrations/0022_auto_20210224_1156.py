# Generated by Django 3.1.2 on 2021-02-24 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_marketing', '0021_coremarketingsetting_final'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coremarketingsetting',
            name='final',
            field=models.BooleanField(unique=True),
        ),
    ]
