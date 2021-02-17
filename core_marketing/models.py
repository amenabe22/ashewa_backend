from uuid import uuid4
from django.db import models
from vendors.models import Vendor, VendorLevelPlans
from accounts.models import CustomUser, Admin, Affilate, CoreLevelPlans
# from .core_manager import UniLevelMarketingNetworkManager
from mptt.models import MPTTModel, TreeForeignKey


class BillingInfo(models.Model):
    binfo_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)

    full_name = models.CharField(max_length=250)
    address = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=300)

    def __str__(self):
        return str(self.binfo_id)

# NEW


class CoreMlmOrders(models.Model):
    order_stats = [
        ('pen', 'Pending Order'),
        ('cmp', 'Completed Order'),
        ('can', 'Cancelled Order')
    ]
    core_order_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    billing_info = models.ForeignKey(
        BillingInfo, on_delete=models.CASCADE, null=True)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        CoreLevelPlans, on_delete=models.CASCADE,  null=True)
    sponsor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, related_name='sponsor', blank=True)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=True, null=True)
    order_status = models.CharField(
        max_length=10, choices=order_stats, default='pen')
    paid_already = models.BooleanField(default=False)

    def __str__(self):
        return str(self.core_order_id)
# NEW


class CoreVendorMlmOrders(models.Model):
    order_stats = [
        ('pen', 'Pending Order'),
        ('cmp', 'Completed Order'),
        ('can', 'Cancelled Order')
    ]
    core_order_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    billing_info = models.ForeignKey(
        BillingInfo, on_delete=models.CASCADE, null=True)
    order_id = models.UUIDField(default=uuid4, editable=False)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered_from = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(
        to='core_ecommerce.Products', on_delete=models.CASCADE,  null=True)
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=True, null=True)
    order_status = models.CharField(
        max_length=10, choices=order_stats, default='pen')
    paid_already = models.BooleanField(default=False)

    def __str__(self):
        return str(self.core_order_id)


class Ewallet(models.Model):
    wallet_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return "{} **{} ETB**".format(self.user.username, self.amount)

class Marketingwallet(models.Model):
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
        if self.affilate.user == self.user:
            return
        if self._state.adding:
            usr = self.affilate.user
            # net = UniLevelMarketingNetworkManager(
            # planid=self.marketing_plan.core_id, plan_type="core")
            if self.user == usr:
                return
            # self.update_aff_net_data()
            # if net.get_max_net(usr) >= self.marketing_plan.count:
            #     # TODO keep the exception just incase
            #     # raise Exception("Reached beyond the predefined layers limit.")
            #     return
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
    core_plan = models.ForeignKey(
        CoreLevelPlans, on_delete=models.CASCADE, null=True, blank=True)
    vendor_plan = models.ForeignKey(
        VendorLevelPlans, on_delete=models.CASCADE, null=True, blank=True)
    total_earned = models.BigIntegerField(null=True, blank=True, default=0)
    total_downline = models.BigIntegerField(null=True, blank=True, default=0)
    total_direct_referrals = models.BigIntegerField(
        null=True, blank=True, default=0)
    total_earned_pv = models.BigIntegerField(null=True, blank=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(str(self.plan_id), self.affilate.user.username)


class UniLevelMarketingNetworkManager(object):
    def __init__(self, planid, plan_type="core"):
        self.planid = planid
        self.plan = None
        self.planSets = {}
        self.plan_type = plan_type
        self.affilate = None
        self.massUsers = []

    def setup_plans(self):
        try:
            # get the selected marketing plan
            if self.plan_type == "core":
                self.plan = CoreLevelPlans.objects.get(
                    core_id=self.planid
                )
            elif self.plan_type == "vendor":
                self.plan = VendorLevelPlans.objects.get(
                    core_id=self.planid
                )
            else:
                raise Exception("Plan type not found")

        except Exception as e:
            print(e)
            raise Exception("plan not found")

    def form_tree(self, usr):
        tree = self.get_genology(usr)['firstSets']
        # print(self.plan)
        for idx, x in enumerate(tree):
            # TODO CHECK BACK HERE
            # if the level is less than plan count
            # if x['level'] < self.plan.count:
            usr_inside_tree = tree[idx]['user'][0]
            tree[idx]['children'] = self.parse_nets(usr_inside_tree)
            tree[idx]['user'] = tree[idx]['user'][0].username

        return tree

    def parse_nets(self, user):
        fin = []
        _gen = self.get_genology(user)
        for x in _gen['firstSets']:
            fin.append({'user': x['user'][0].username,
                        'children': self.form_tree(x['user'][0]),
                        'core_level': x['level']})
        return fin

    def get_net_by_lvl(self, nets, cnt):
        fin_netpack = []
        for nt in nets:
            if nt['core_level'] == cnt:
                print(nt['core_level'], cnt)
                fin_netpack.append(nt)
            # else:
            #     raise Exception("Level not reached yet")
        return fin_netpack

    def get_max_net(self, user: CustomUser):
        _net_lvls = []
        [_net_lvls.append(int(x['core_level']))
            for x in self.parse_nets(user=user)]
        return max(_net_lvls)

    def get_all_nets(self, user: CustomUser):
        self.setup_plans()
        # DOES return only the first level
        return self.get_net_by_lvl(self.parse_nets(user), 1)
        # return self.parse_nets(user)
        # for x in _gen['firstSets']:
        #     self.massUsers.append(x['user'][0])
        # self.get_mass_genology(self.massUsers)
        # pprint(self.planSets['firstSets'])
        # print(self.check_affilate_status(x['user'][0]))
        # [pprint(self.get_genology(x)) for x in self.massUsers]

    def check_affilate_status(self, user):
        return Affilate.objects.filter(user=user).exists()

    def get_genology(self, user: CustomUser):
        self.setup_plans()
        self.planSets = {'firstSets': [], 'secondSets': [], 'thirdSets': [],
                         'fourth': [], 'fivth': [], 'sixth': []}
        try:
            self.affilate = Affilate.objects.get(
                user=user
            )
        except:
            self.affilate = None

        curr_affilate = self.affilate
        all_aff_nets = UnilevelNetwork.objects.filter(
            marketing_plan=self.plan, affilate=curr_affilate)

        for x in all_aff_nets:
            self.planSets['firstSets'].append({'user': CustomUser.objects.filter(
                user_id=x.user.user_id), 'level': 1})

        lstIdxs = list(self.planSets.keys())
        for idx, (mn, sn) in enumerate(zip(lstIdxs, lstIdxs[1:])):
            for x in self.planSets[mn]:
                if self.check_affilate_status(x['user'][0]):
                    nets = UnilevelNetwork.objects.filter(marketing_plan=self.plan,
                                                          affilate=Affilate.objects.get(
                                                              user=x['user'][0]))
                    for i in nets:
                        self.planSets[sn].append({'user': CustomUser.objects.filter(
                            user_id=i.user.user_id
                        ), 'level': idx+2})
        allIdx = []
        for l in range(len(lstIdxs)):
            allIdx.append(l)
        for x in sorted(allIdx, reverse=True):
            [self.planSets[lstIdxs[x-1]].append(fin)
             for fin in self.planSets[lstIdxs[x]]]
        return self.planSets


# test networks model for management
class TestNetwork(models.Model):
    layer_id = models.UUIDField(
        default=uuid4, editable=False, primary_key=True)
    marketing_plan = models.ForeignKey(
        CoreLevelPlans, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='kids', on_delete=models.CASCADE)

    affilate = models.ForeignKey(
        Affilate, on_delete=models.CASCADE, null=True)
    # user is the child
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # level = models.IntegerField(null=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserMessages(models.Model):
    full_name = models.CharField(max_length=800)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email


class CoreDocs(models.Model):
    name = models.CharField(max_length=300)
    doc = models.FileField(upload_to='core/docs')

    def __str__(self):
        return self.name


# Core test mptt
class CoreTestMpttNode(MPTTModel):
    # parent = models.ForeignKey("self", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    marketing_plan = models.ForeignKey(
        CoreLevelPlans, on_delete=models.CASCADE, null=True)

    class MPTTMeta:
        order_insertion_by = ['user']

    def __str__(self):
        return "{} called {} ===>[[{}]]<===".format(self.parent, self.user, self.marketing_plan.plan_name)

    def initiate_nodes_logic(self):
        print("CUR PARENT => {}".format(self.parent.user))
        print("CUR USR => {}".format(self.user))
        print("I will pay every one what they deserve")

# Core test mptt
class CoreVendorTestMpttNode(MPTTModel):
    # parent = models.ForeignKey("self", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    marketing_plan = models.ForeignKey(
        VendorLevelPlans, on_delete=models.CASCADE, null=True)

    class MPTTMeta:
        order_insertion_by = ['user']

    def __str__(self):
        return "{} called {} ===>[[{}]]<===".format(self.parent, self.user, self.marketing_plan.plan_name)

    def initiate_nodes_logic(self):
        print("CUR PARENT => {}".format(self.parent.user))
        print("CUR USR => {}".format(self.user))
        print("I will pay every one what they deserve")
