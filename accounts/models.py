from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
# from core_marketing.models import Rank
# from core_marketing.models import CoreLevelPlans


class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    phone = models.BigIntegerField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    full_name = models.CharField(max_length=800, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


class UserProfile(models.Model):
    profile_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=400, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="profile/pics", blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}".format(self.full_name)


class Admin(models.Model):
    admin_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)


class StaffPrivillage(models.Model):
    staff_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True)
    business_setting = models.BooleanField(default=False)
    user_view = models.BooleanField(default=False)
    user_management = models.BooleanField(default=False)
    wallet_management = models.BooleanField(default=False)
    epin_management = models.BooleanField(default=False)
    earning_management = models.BooleanField(default=False)
    manage_product = models.BooleanField(default=False)
    view_orders = models.BooleanField(default=False)
    manage_brand = models.BooleanField(default=False)
    manage_report = models.BooleanField(default=False)
    manage_expense = models.BooleanField(default=False)
    manage_support = models.BooleanField(default=False)

    def __str__(self):
        return str(self.staff_id)


class RepurchaseBonusLevel(models.Model):
    level_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True, unique=True)
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
        return str(self.level_id)


class CoreLevelPlans(models.Model):
    core_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    creator = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)
    # optional multi level percentages
    plan_name = models.CharField(max_length=500, null=True)
    is_repurchase = models.BooleanField(default=False)
    repurchase_level = models.ForeignKey(
        RepurchaseBonusLevel, on_delete=models.CASCADE, null=True, blank=True)
    joining_fee = models.FloatField(
        default=0.0, null=True)
    joining_pv = models.IntegerField(
        default=0, null=True, blank=True, help_text="the joining credit award package")
    has_purchase_bonus = models.BooleanField(default=False, null=True)
    purchase_bonus = models.IntegerField(default=0, null=True)
    plan_image = models.ImageField(
        upload_to='plan/image/', null=True, blank=True)
    show_plan_form = models.BooleanField(default=False)
    plan_description = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0, null=True, blank=True)
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


class Rank(models.Model):
    rank_opts = [
        ('maint', 'Main Target'),
        ('downt', 'Downline Target')
    ]
    cnt_basedon = [
        ('pvval', 'Pv Value'),
        ('memcnt', 'Members Count')
    ]
    rank_id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    rank_name = models.CharField(max_length=500)
    # based_on = models.CharField(max_length=5, choices=rank_opts)
    count_based_on = models.CharField(max_length=6, choices=cnt_basedon)
    # duration = models.BigIntegerField(default=0, null=True, blank=True)
    # downline_value = models.BigIntegerField(null=True, blank=True)
    # direct_referrals = models.BigIntegerField(null=True, blank=True)
    # total pv count ranged input
    total_pv_count_start = models.BigIntegerField(
        null=True, default=0, blank=True)
    total_pv_count_end = models.BigIntegerField(
        null=True, default=0, blank=True)
    # notice that above
    # level_no = models.IntegerField(null=True, blank=True)
    # total_member_on_level = models.BigIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rank_name


class Affilate(models.Model):
    affilate_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.Model)
    # test Field
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    affilate_rank = models.ForeignKey(
        Rank, on_delete=models.CASCADE, null=True, blank=True)
    total_teams = models.BigIntegerField(null=True, blank=True)
    total_pv = models.BigIntegerField(null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def save_mplan_data(self, all_direct, total_earned, total_downline, mplan):
        # aff = Affilate.objects.get(user=self.user)
        # print(AffilatePlans.objects.get(affilate=self))
        # sponsors_aff_plan = AffilatePlans.objects.get(
        #     affilate=self, core_plan=mplan, plan_type='core')
        # sponsors_aff_plan.total_direct_referrals = all_direct
        # sponsors_aff_plan.total_earned = total_earned
        # sponsors_aff_plan.total_downline = total_downline
        # sponsors_aff_plan.save()
        # print(mplan,"PLEASEEEE LORD")
        pass
