# Generated by Django 3.1.2 on 2021-02-07 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core_marketing', '0001_initial'),
        ('core_ecommerce', '0001_initial'),
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_marketing.corebrand'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core_ecommerce.category'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_images',
            field=models.ManyToManyField(blank=True, to='core_ecommerce.ProductImage'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_parent_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_ecommerce.parentcategory'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core_ecommerce.subcategory'),
        ),
        migrations.AddField(
            model_name='products',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor'),
        ),
        migrations.AddField(
            model_name='products',
            name='vendor_plans',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendorlevelplans'),
        ),
        migrations.AddField(
            model_name='parentcategory',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_marketing.corebrand'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core_ecommerce.parentcategory'),
        ),
    ]
