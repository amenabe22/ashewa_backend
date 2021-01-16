from uuid import uuid4
from django.db import models
from core_marketing.models import CoreBrand
from vendors.models import Vendor, VendorLevelPlans


class ParentCategory(models.Model):
    pcat_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    parent_cat_name = models.CharField(max_length=500)
    brand = models.ForeignKey(CoreBrand, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    cat_decs = models.TextField(null=True, blank=True)
    cat_image = models.ImageField(
        upload_to='pcat-image/', null=True, blank=True)

    def __str__(self):
        return self.parent_cat_name


class Category(models.Model):
    cat_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    category_name = models.CharField(max_length=500, null=True)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_cat_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    sub_category_name = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.sub_category_name


class ProductImage(models.Model):
    image = models.ImageField(upload_to="prod/images/")
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)


class Products(models.Model):
    product_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=800)
    product_desc = models.TextField(null=True)
    product_parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE)
    product_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    product_subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True)
    product_brand = models.ForeignKey(CoreBrand, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)
    selling_price = models.BigIntegerField(null=True)
    dealer_price = models.BigIntegerField(null=True)
    # product_cost
    business_value = models.BigIntegerField(help_text="PV", null=True)
    discount = models.FloatField(default=0.0, null=True)
    stock_amount = models.BigIntegerField(default=1, null=True)
    tax = models.FloatField(default=0.0, null=True)
    product_images = models.ManyToManyField(ProductImage, blank=True)
    vendor_plans = models.ForeignKey(
        VendorLevelPlans, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name


class LandingCarousel(models.Model):
    car_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    image = models.ImageField(upload_to='landing/car')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.car_id)
