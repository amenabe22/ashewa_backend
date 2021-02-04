# Generated by Django 3.1.2 on 2021-02-04 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0013_auto_20210113_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenodrGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='venodr/gallery')),
                ('img_desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='vendor',
            name='store_gallery',
            field=models.ManyToManyField(blank=True, to='vendors.VenodrGallery'),
        ),
    ]