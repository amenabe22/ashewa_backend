# Generated by Django 3.1.2 on 2021-02-07 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_affilate_parent'),
        ('core_marketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coretestmpttnode',
            name='marketing_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.corelevelplans'),
        ),
    ]
