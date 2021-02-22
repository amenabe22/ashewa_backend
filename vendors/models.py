from django.db import models
from uuid import uuid4
from accounts.models import CustomUser
from django.db import models
# Create your models here.


class VenodrGallery(models.Model):
    image = models.ImageField(upload_to='venodr/gallery')
    img_desc = models.TextField(null=True, blank=True)


class Vendor(models.Model):
    vendor_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.Model)
    store_name = models.CharField(max_length=800, null=True, blank=True)
    store_cover = models.ImageField(
        upload_to='store/image', null=True, blank=True)
    store_gallery = models.ManyToManyField(VenodrGallery, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


class VendorLevelPlans(models.Model):
    core_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    creator = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    # optional multi level percentages
    plan_name = models.CharField(max_length=500, null=True)
    # joining_fee = models.FloatField(default=0.0, null=True)
    # plan_image = models.ImageField(
    #     upload_to='plan/image/', null=True, blank=True)
    show_plan_form = models.BooleanField(default=False)
    purchase_bonus = models.FloatField(
        null=True, blank=True, help_text='bonus amount')
    plan_description = models.TextField(null=True, blank=True)
    level1_percentage = models.FloatField(
        default=0.0, null=True, blank=True, help_text="First core level")
    level2_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level3_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level4_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level5_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level6_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level7_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level8_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level9_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level10_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level11_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level12_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level13_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level14_percentage = models.FloatField(default=0.0, null=True, blank=True)
    level15_percentage = models.FloatField(default=0.0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.plan_name)


class Cart(models.Model):
    cart_core_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    cart_id = models.UUIDField(
        default=uuid4, editable=False)
    user = models.ForeignKey(to='accounts.CustomUser',
                             on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        to='core_ecommerce.Products', on_delete=models.CASCADE)
    quantity = models.BigIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_core_id)


class Order(models.Model):
    order_stats = [
        ('pen', 'Pending Order'),
        ('cmp', 'Completed Order'),
        ('can', 'Cancelled Order')
    ]
    core_order_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    billing_info = models.ForeignKey(
        to='core_marketing.BillingInfo', on_delete=models.CASCADE, null=True)
    order_id = models.UUIDField(default=uuid4, editable=False)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered_from = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(
        to='core_ecommerce.Products', on_delete=models.CASCADE, blank=True, null=True)
    # product = models.ForeignKey(
    #     to='core_ecommerce.Products', on_delete=models.CASCADE,  null=True)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=True, null=True)
    order_status = models.CharField(
        max_length=10, choices=order_stats, default='pen')

    def __str__(self):
        return str(self.core_order_id)

class Social(models.Model):
    social_name = models.CharField(max_length=100)
    social_icon = models.CharField(max_length=100)
    icon_color = models.CharField(max_length=100, null=True)
    social_link = models.URLField(('social_link'), max_length=300, null=True)

class VendorCeoImgs(models.Model):
    ceo_img = models.ImageField(upload_to='about/ceo/image', null=True)

class VendorData(models.Model):
    store_name = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True)
    store_desc = models.TextField(null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    images = models.ManyToManyField(VendorCeoImgs, blank=True)
    social_net = models.ManyToManyField(Social, blank=True)
    video_url = models.URLField(("video_url"), max_length=300)

    def __str__(self):
        return self.email
    