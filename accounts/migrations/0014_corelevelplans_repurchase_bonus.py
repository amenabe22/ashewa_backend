# Generated by Django 3.1.2 on 2021-03-04 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210228_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='corelevelplans',
            name='repurchase_bonus',
            field=models.IntegerField(default=0, null=True),
        ),
    ]