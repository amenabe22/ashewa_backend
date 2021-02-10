# Generated by Django 3.1.2 on 2021-02-10 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_marketing', '0010_coremlmorders_sponsor'),
    ]

    operations = [
        migrations.AddField(
            model_name='corevendormlmorders',
            name='paid_already',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coremlmorders',
            name='sponsor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsorZ', to=settings.AUTH_USER_MODEL),
        ),
    ]