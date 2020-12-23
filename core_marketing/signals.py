from accounts.models import Affilate, CustomUser
from pprint import pprint
from django.db.models.signals import post_save
from django.dispatch import receiver
from .core_manager import UniLevelMarketingNetworkManager
from.models import UnilevelNetwork, AffilatePlans


@receiver(post_save, sender=UnilevelNetwork)
def my_handler(sender, instance, **kwargs):
    join_fee = instance.marketing_plan.joining_fee
    net = UniLevelMarketingNetworkManager(
        planid=instance.marketing_plan.core_id, plan_type="core")
    affNet = AffilatePlans.objects.filter(
        affilate=instance.affilate, core_plan=instance.marketing_plan)

    firstLevels = net.get_net_by_lvl(net.parse_nets(instance.affilate.user), 1)
    # print(firstLevels, "AGAIN")

    totalDowns = 0
    # print(self.marketing_plan, self.affilate.user, "TEST")
    totalDownUsrs = []
    total_lvl1_income = 0
    total_downline_income_main = 0
    for i in range(instance.marketing_plan.count):
        if i > 1:
            allLens = net.get_net_by_lvl(
                net.parse_nets(instance.affilate.user), i)
            print(allLens, i, instance.affilate.user)
            [totalDownUsrs.append(x['user']) for x in allLens]
            # print("#"*20)
            # print(allLens)
            # # print()
            # # print(len(allLens), "@@@", allLens, "==> % d" % i)
            # print()
            totalDowns += len(allLens)
            cut_amount_main = instance.marketing_plan.__dict__[
                'level{}_percentage'.format(i)]
            if cut_amount_main > 0:  # check if the amount is greater than 0
                # this is the amount per this level
                print(instance.affilate.user.username, "====", "LEVEL {}".format(
                    i), "AMT ", cut_amount_main, " JOINING FEE ", join_fee)

    # pass the downline amounts and update everyone's data i the network
                # print("CORE LVL 1", cut_lvl1_amount_main)
                total_downline_income_main += join_fee * cut_amount_main
                print(total_downline_income_main, "GROWWW")
                # print("CORE Downline", total_downline_income_main)
        else:
            total_lvl1_income += join_fee * instance.marketing_plan.level1_percentage
            pass
    # cut_lvl1_amount_main = join_fee * instance.marketing_plan.level1_percentage
    total_earned_main = total_lvl1_income + total_downline_income_main
    print(totalDowns, "Total Downlines")
    affNet.update(total_direct_referrals=len(
        firstLevels), total_downline=totalDowns, total_earned=total_earned_main)

    print(totalDownUsrs,"NIGGGA")
    for aff in totalDownUsrs:
        usr = CustomUser.objects.filter(username=aff)
        aff = Affilate.objects.filter(user=usr[0])
        # print(CustomUser.objects.filter(
        #             username=aff
        #         ).exists(),"@"*200)
        if aff.exists():
            allAffNets = AffilatePlans.objects.filter(
                affilate=Affilate.objects.get(
                    user=usr[0]
                )
            )
            allFirstLevels = net.get_net_by_lvl(
                net.parse_nets(usr[0]), 1)
            print(allFirstLevels, "!!!!!"*20)
            alltotalDownUsrs = 0
            cut_lvl1_amount = 0
            for i in range(instance.marketing_plan.count):
                if i > 1:
                    allLens = net.get_net_by_lvl(
                        net.parse_nets(usr[0]), i)
                    alltotalDownUsrs += len(allLens)
                    # cur amount is the amount they get per that level
                    cut_amount = instance.marketing_plan.__dict__[
                        'level{}_percentage'.format(i)]
                    if cut_amount > 0:  # check if the amount is greater than 0
                        # this is the amount per this level
                        print(usr[0].username, "====", "LEVEL {}".format(
                            i), "AMT ", cut_amount, " JOINING FEE ", instance.marketing_plan.joining_fee)
                    # join_fee = instance.marketing_plan.joining_fee
                else:
                    # level one for the downs go here
                    cut_lvl1_amount += join_fee * instance.marketing_plan.level1_percentage
            print(total_lvl1_income,"DOWNS")
            total_downline_income = join_fee * cut_amount
            total_earned = cut_lvl1_amount + total_downline_income
            allAffNets.update(total_direct_referrals=len(
                allFirstLevels), total_downline=alltotalDownUsrs, total_earned=int(total_earned))
