# Generated by Django 3.1.2 on 2021-02-10 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_affilate_parent'),
        ('core_marketing', '0002_coretestmpttnode_marketing_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='coretestmpttnode',
            name='affilate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.affilate'),
        ),
    ]