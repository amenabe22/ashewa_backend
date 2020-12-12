from uuid import uuid4
from django.db import models
from vendors.models import Vendor, VendorLevelPlans
from accounts.models import CustomUser, Admin, Affilate, CoreLevelPlans


class Ewallet(models.Model):
    wallet_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return "{} **{} ETB**".format(self.user.username, self.amount)


class CoreBrand(models.Model):
    brand_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    brand_name = models.CharField(max_length=500)
    brand_description = models.TextField(null=True)
    brand_image = models.ImageField(upload_to='brand-pics/', null=True)

    def __str__(self):
        return self.brand_name


class UnilevelNetwork(models.Model):
    layer_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    marketing_plan = models.ForeignKey(
        CoreLevelPlans, on_delete=models.CASCADE, null=True)
    affilate = models.ForeignKey(Affilate, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # level = models.IntegerField(null=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(self.affilate.user.username, self.user.username)

    def save(self, *args, **kwargs):
        all_other_current_nets = UnilevelNetwork.objects.filter(
            marketing_plan=self.marketing_plan).exclude(layer_id=self.layer_id)
        print(all_other_current_nets)
        super(UnilevelNetwork, self).save(*args, **kwargs)


class Rewards(models.Model):
    reward_opts = [
        ('maint', 'Main Target'),
        ('downt', 'Downline Target')
    ]
    cnt_basedon = [
        ('pvval', 'Pv Value'),
        ('memcnt', 'Members Count')
    ]
    reward_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    plan = models.ForeignKey(CoreLevelPlans, on_delete=models.CASCADE)
    reward_name = models.CharField(max_length=700)
    reward_based_on = models.CharField(max_length=6, choices=reward_opts)
    count_based_on = models.CharField(max_length=6, choices=cnt_basedon)
    duration = models.BigIntegerField(default=0)
    downline_value = models.BigIntegerField(null=True, blank=True)
    direct_referrals = models.BigIntegerField(null=True, blank=True)
    level_no = models.IntegerField(null=True, blank=True)
    total_member_on_level = models.BigIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.reward_id)


class PayoutReport(models.Model):
    stat = [('cmp', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')]

    payout_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    admin_fee = models.IntegerField()
    tax = models.IntegerField()
    net_amount = models.IntegerField()
    mode = models.CharField(max_length=50)
    account_detail = models.TextField()
    status = models.CharField(max_length=5, choices=stat)
    transaction_detail = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payout_id)


class DepositReport(models.Model):
    stats = [('cmp', 'Completed'), ('pen', 'Pending'), ('can', 'Cancelled')]
    gateways = [('bnk', 'Bank')]
    transaction_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gateway = models.CharField(max_length=5, choices=gateways)
    status = models.CharField(max_length=12, choices=stats)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.transaction_id)


class AffilatePlans(models.Model):
    pl_types = [
        ('core', 'Core Plans'),
        ('ven', 'Vendor Plan'),
    ]
    plan_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    affilate = models.ForeignKey(Affilate, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=5, choices=pl_types, null=True)
    core_plan = models.OneToOneField(
        CoreLevelPlans, on_delete=models.CASCADE, null=True, blank=True)
    vendor_plan = models.OneToOneField(
        VendorLevelPlans, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.plan_id)
