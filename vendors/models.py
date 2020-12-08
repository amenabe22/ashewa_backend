from django.db import models
from uuid import uuid4
from accounts.models import CustomUser
# Create your models here.


class Vendor(models.Model):
    vendor_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.Model)
    store_name = models.CharField(max_length=800, null=True, blank=True)
    store_desc = models.TextField(blank=True, null=True)
    store_cover = models.ImageField(
        upload_to='store/image', null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


class VendorLevelPlans(models.Model):
    core_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    creator = models.OneToOneField(Vendor, on_delete=models.CASCADE)
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

    def __str__(self):
        return str(self.plan_name)
