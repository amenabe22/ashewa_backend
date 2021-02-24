# Generated by Django 3.1.2 on 2021-02-23 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_affilate_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='corelevelplans',
            name='joining_pv',
            field=models.FloatField(blank=True, default=0.0, help_text='the joining credit award package', null=True),
        ),
    ]
