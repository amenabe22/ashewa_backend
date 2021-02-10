from pprint import pprint
from django.db.models.signals import post_save
from django.dispatch import receiver
from .core_manager import UniLevelMarketingNetworkManager
from accounts.models import Affilate, CustomUser, CoreLevelPlans
from .models import UnilevelNetwork, AffilatePlans, CoreMlmOrders, CoreTestMpttNode, Ewallet


@receiver(post_save, sender=CoreMlmOrders)
def core_mlm_order_approval_handler(sender, instance, **kwargs):
    if not instance.paid_already:
        if instance.order_status == 'cmp':
            # order is completed so trigger message here
            # Award sponsor here
            sponsor = CoreTestMpttNode.objects.get(user=instance.sponsor)
            allAncestors = sponsor.get_ancestors(
                include_self=True, ascending=True).order_by('level')
            print("#"*20)
            print(sponsor.get_descendants(), "YEAA")
            money = instance.product
            print("$"*20)
            print()
            # fare = money.
            # print(money)
            print("$"*20)
            allLvl = []
            print(allAncestors)
            [allLvl.append({'lvl': x.level, 'usr':str(x.user.user_id)}) for x in allAncestors]
            # print(allLvl,"LLLL")
            # print(allLvl[::-1],"PLEASE")
            # [allLvl.append({'lvl': x.level, 'usr': x.user.user_id})
            #  for x in allAncestors]
            allLvl = allLvl[::-1]
            print(allLvl,"EEE")
            for usrs,x  in zip(allAncestors, allLvl):
                print(x,"UAA")
                # po = filter(lambda y: y['usr'] == usrs.user.user_id, allLvl)
                # print(list(po), "YEA")
                # print('level{}_percentage'.format(
                #     usrs.level+1), "===", usrs.user)
                aff = Affilate.objects.get(user=usrs.user)
                affWallet = Ewallet.objects.get(
                    user=usrs.user
                )
                fare = money.__dict__[
                    'level{}_percentage'.format(x['lvl']+1)]
                print(fare, "FAREEE", "{} GIVEN TO {} LEVEL->{}".format(fare,
                                                                        usrs.user, usrs.level+1))
                affWallet.amount += money.joining_fee * fare
                affWallet.save()
                print(aff, "FARE = {}".format(fare),
                      "AMT {}".format(money.joining_fee))
            instance.paid_already = True
            instance.save()
            print("#"*20)
            pass
# Core MLM orders


# @receiver(post_save, sender=UnilevelNetwork)
# def my_handler(sender, instance, **kwargs):
#     join_fee = instance.marketing_plan.joining_fee
#     net = UniLevelMarketingNetworkManager(
#         planid=instance.marketing_plan.core_id, plan_type="core")
#     affNet = AffilatePlans.objects.filter(
#         affilate=instance.affilate, core_plan=instance.marketing_plan)

#     firstLevels = net.get_net_by_lvl(net.parse_nets(instance.affilate.user), 1)
#     # print(firstLevels, "AGAIN")
#     allLvl1 = []
#     totalDowns = 0
#     # print(self.marketing_plan, self.affilate.user, "TEST")
#     totalDownUsrs = []
#     total_lvl1_income = 0
#     total_downline_income_main = 0
#     for j in range(instance.marketing_plan.count):
#         i = j+1
#         # if i > 1:
#         allLens = net.get_net_by_lvl(
#             net.parse_nets(instance.affilate.user), i)
#         # print(len(allLens) > 0, i, "DIDE")
#         # print(instance.affilate.user, "PLEASE")
#         print(allLens, "()"*10, "==>", i)
#         if (len(allLens) > 0) and i > 1:
#             # print(allLens, "BRO", i)
#             [totalDownUsrs.append(x['user']) for x in allLens]
#             # print("#"*20)
#             # print(allLens)
#             # # print()
#             # # print(len(allLens), "@@@", allLens, "==> % d" % i)
#             # print()
#             totalDowns += len(allLens)
#             cut_amount_main = instance.marketing_plan.__dict__[
#                 'level{}_percentage'.format(i)]
#             if cut_amount_main > 0:  # check if the amount is greater than 0
#                 # this is the amount per this level
#                 print(instance.affilate.user.username, "====", "LEVEL {}".format(
#                     i), "AMT ", cut_amount_main, " JOINING FEE ", join_fee)

#                 # print("CORE LVL 1", cut_lvl1_amount_main)
#                 total_downline_income_main += join_fee * cut_amount_main
#                 # print(total_downline_income_main, "GROWWW")
#         else:
#             for po in allLens:
#                 total_lvl1_income += join_fee * instance.marketing_plan.level1_percentage

#             # if len(allLens) > 0:
#             #     print(, "REALLY")
#             #     print("this is level one")
#             # total_lvl1_income += join_fee * instance.marketing_plan.level1_percentage
#             # allLvl1.append(total_lvl1_income)
#             # print(i)
#             # print("CORE Downline", total_downline_income_main)
#         # else: print(len(allLens),"DOOO")
#         # # DO LEVEL ONE
#         # else:
#         #     total_lvl1_income += join_fee * instance.marketing_plan.level1_percentage
#         #     pass
#     # cut_lvl1_amount_main = join_fee * instance.marketing_plan.level1_percentage
#     print(allLvl1, "!@!!")
#     total_earned_main = total_lvl1_income + total_downline_income_main
#     print(totalDowns, "Total Downlines")
#     affNet.update(total_direct_referrals=len(
#         firstLevels), total_downline=totalDowns, total_earned=total_earned_main)

#     print(totalDownUsrs, "NIGGGA")
#     for aff in totalDownUsrs:
#         usr = CustomUser.objects.filter(username=aff)
#         aff = Affilate.objects.filter(user=usr[0])
#         # print(CustomUser.objects.filter(
#         #             username=aff
#         #         ).exists(),"@"*200)
#         if aff.exists():
#             allAffNets = AffilatePlans.objects.filter(
#                 affilate=Affilate.objects.get(
#                     user=usr[0]
#                 )
#             )
#             allFirstLevels = net.get_net_by_lvl(
#                 net.parse_nets(usr[0]), 1)
#             print(allFirstLevels, "!!!!!"*20)
#             alltotalDownUsrs = 0
#             cut_lvl1_amount = 0
#             for i in range(instance.marketing_plan.count):
#                 # i = j+1

#                 allLens = net.get_net_by_lvl(
#                     net.parse_nets(usr[0]), i)
#                 # if len(allLens) > 0 and (i > 1):
#                 if i > 1:

#                     alltotalDownUsrs += len(allLens)
#                     # cur amount is the amount they get per that level
#                     cut_amount = instance.marketing_plan.__dict__[
#                         'level{}_percentage'.format(i)]
#                     if cut_amount > 0:  # check if the amount is greater than 0
#                         # this is the amount per this level
#                         print(usr[0].username, "====", "LEVEL {}".format(
#                             i), "AMT ", cut_amount, " JOINING FEE ", instance.marketing_plan.joining_fee)
#                     # join_fee = instance.marketing_plan.joining_fee
#                 else:
#                     # level one for the downs go here
#                     cut_lvl1_amount += join_fee * instance.marketing_plan.level1_percentage
#             print(total_lvl1_income, "DOWNS")
#             total_downline_income = join_fee * cut_amount
#             total_earned = cut_lvl1_amount + total_downline_income
#             allAffNets.update(total_direct_referrals=len(
#                 allFirstLevels), total_downline=alltotalDownUsrs, total_earned=int(total_earned))
