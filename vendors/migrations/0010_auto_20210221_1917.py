# Generated by Django 3.1.2 on 2021-02-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0009_vendordata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendordata',
            name='video_url',
            field=models.URLField(max_length=300, verbose_name='video_url'),
        ),
    ]
