# Generated by Django 3.1.2 on 2020-12-03 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='store_cover',
            field=models.ImageField(blank=True, null=True, upload_to='store/image'),
        ),
    ]
