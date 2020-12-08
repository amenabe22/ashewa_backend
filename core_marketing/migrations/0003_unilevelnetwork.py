# Generated by Django 3.1.2 on 2020-12-06 06:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_full_name'),
        ('vendors', '0006_vendorlevelplans_purchase_bonus'),
        ('core_marketing', '0002_auto_20201206_0639'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnilevelNetwork',
            fields=[
                ('layer_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(help_text='network level count')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('affilate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.affilate')),
                ('marketing_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.corelevelplans')),
                ('vendor_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendorlevelplans')),
            ],
        ),
    ]
