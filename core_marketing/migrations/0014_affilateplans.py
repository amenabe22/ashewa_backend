# Generated by Django 3.1.2 on 2020-12-11 17:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_corelevelplans_count'),
        ('core_marketing', '0013_remove_unilevelnetwork_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffilatePlans',
            fields=[
                ('plan_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('affilate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.affilate')),
            ],
        ),
    ]
