# Generated by Django 3.1.2 on 2020-12-11 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0006_vendorlevelplans_purchase_bonus'),
        ('accounts', '0005_corelevelplans_count'),
        ('core_marketing', '0015_auto_20201211_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affilateplans',
            name='core_plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.corelevelplans'),
        ),
        migrations.AlterField(
            model_name='affilateplans',
            name='vendor_plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendorlevelplans'),
        ),
    ]
