# Generated by Django 3.1.2 on 2021-02-28 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210228_0913'),
        ('core_marketing', '0023_auto_20210225_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rewards',
            name='direct_referrals',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='downline_value',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='level_no',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='reward_based_on',
        ),
        migrations.RemoveField(
            model_name='rewards',
            name='total_member_on_level',
        ),
        migrations.AddField(
            model_name='rewards',
            name='rank',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.rank'),
        ),
    ]
