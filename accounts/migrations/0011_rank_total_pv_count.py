# Generated by Django 3.1.2 on 2021-02-28 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210223_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='total_pv_count',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
