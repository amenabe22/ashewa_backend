from pprint import pprint
from django.db.models.signals import post_save
from django.dispatch import receiver
from .core_manager import UniLevelMarketingNetworkManager
from accounts.models import Affilate, CustomUser, CoreLevelPlans, Rank
from .models import (UnilevelNetwork, AffilatePlans, CoreMlmOrders, CoreVendorTestMpttNode,
                     CoreTestMpttNode, Ewallet, Marketingwallet, CoreVendorMlmOrders, Rewards, RewardsReport)
from core_marketing.models import CoreMarketingSetting
from django.core.mail import send_mail
from django.conf import settings


def core_mail_sender(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)
    print("EMAIL SENT")


@receiver(post_save, sender=CoreVendorMlmOrders)
def core_vendor_mlm_order_approval_handler(sender, instance, **kwargs):
    if not instance.paid_already:
        if instance.order_status == 'cmp':
            # order is completed so trigger message here
            # Award sponsor here
            # what if there is noone yet
            global sponsor
            affilate = Affilate.objects.filter(
                user=instance.ordered_by
            )
            markallet = Marketingwallet.objects.filter(
                user=instance.ordered_by
            )
            if not markallet.exists():
                Marketingwallet.objects.create(
                    user=instance.ordered_by
                )
            if not affilate.exists():
                affilate = Affilate.objects.create(
                    user=instance.ordered_by
                )
            elif affilate.exists():
                affilate = affilate[0]
            AffilatePlans.objects.create(
                affilate=affilate,
                plan_type='ven',
                vendor_plan=instance.product,
            )

            if CoreVendorTestMpttNode.objects.filter(marketing_plan=instance.product).exists():
                # get the sponsor from the valid input
                sponsor = CoreVendorTestMpttNode.objects.get(
                    user=instance.sponsor, marketing_plan=instance.product)
                allAncestors = sponsor.get_ancestors(
                    include_self=True, ascending=True).order_by('level')
                money = instance.product
                # fare = money.
                allLvl = []
                [allLvl.append({'lvl': x.level, 'usr': str(x.user.user_id)})
                 for x in allAncestors]
                # reverse the list to reverse the levels
                allLvl = allLvl[::-1]
                allDescendants = sponsor.get_descendants()
                allDirect = []
                allDown = []
                [allDirect.append(x) for x in allDescendants if (x.level == 1)]
                [allDown.append(x) for x in allDescendants if (x.level > 1)]
                for usrs, x in zip(allAncestors, allLvl):
                    aff = Affilate.objects.get(user=usrs.user)
                    mWallet = Marketingwallet.objects.get(
                        user=usrs.user
                    )
                    affWallet = Ewallet.objects.get(
                        user=usrs.user
                    )
                    fare = money.__dict__[
                        'level{}_percentage'.format(x['lvl']+1)]
                    print(fare, "FAREEE", "{} GIVEN TO {} LEVEL->{}".format(fare,
                                                                            usrs.user, usrs.level+1))
                    affWallet.amount += money.purchase_bonus * fare
                    affWallet.save()
                    mWallet.amount += money.purchase_bonus * fare
                    mWallet.save()
                    print(aff, "FARE = {}".format(fare),
                          "AMT {}".format(money.purchase_bonus))
                    aff.save_mplan_data(
                        len(allDirect), mWallet.amount, len(allDown), money)
                CoreVendorTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=sponsor
                )
            else:
                CoreVendorTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=None
                )

            instance.paid_already = True
            instance.save()

            print("#"*20)


def reward_ranks(ancestors):
    for anc in ancestors:
        mWallet = Marketingwallet.objects.get(
            user=anc.user
        )
        elligiableRanksQset = Rank.objects.filter(
            count_based_on='pvval'
        )
        affilate = Affilate.objects.get(user=anc.user)
        for elRank in elligiableRanksQset:
            print("RANK {}", format(elRank.rank_name))
            if (elRank.total_pv_count_start <= mWallet.pv_count <= elRank.total_pv_count_end):
                print("USER IS ELLIGIABLE FOR {} RANK".format(elRank.rank_name))
                affilate.affilate_rank = elRank
                affilate.save()
        reward = Rewards.objects.filter(rank=affilate.affilate_rank)
        if reward.exists():

            if not RewardsReport.objects.filter(affilate=affilate, reward=reward[0]).exists():
                reward_report = RewardsReport.objects.create(
                    affilate=affilate, reward=reward[0]
                )
                print("REWARD {} GIVEN TO {}".format(
                    reward_report.reward.reward_name, affilate.user.email))
                emailMessage = """<h2>Congratulations !!!!</h2> \nYou have achieved the Ashewa {} Reward.\nYou can contact us at {} and we will be intouch with you with details of your reward. \n Thanks For working with Ashewa !!!""".format(
                    reward[0].reward_name, "0911928233"
                )
                emailSubject = "Ashewa Reward Achievement"
                core_mail_sender(emailSubject, emailMessage,
                                 [affilate.user.email])
            else:
                print("Affilate has already taken the reward")
            # give out reward here
            # give out rewards


@receiver(post_save, sender=CoreMlmOrders)
def core_mlm_order_approval_handler(sender, instance, **kwargs):
    if not instance.paid_already:
        if instance.order_status == 'cmp':
            # order is completed so trigger message here
            # Award sponsor here
            # what if there is noone yet
            global sponsor
            affilate = Affilate.objects.filter(
                user=instance.ordered_by
            )
            markallet = Marketingwallet.objects.filter(
                user=instance.ordered_by
            )
            if not markallet.exists():
                Marketingwallet.objects.create(
                    user=instance.ordered_by
                )
            if not affilate.exists():
                affilate = Affilate.objects.create(
                    user=instance.ordered_by
                )
            elif affilate.exists():
                affilate = affilate[0]
            AffilatePlans.objects.create(
                affilate=affilate,
                plan_type='core',
                core_plan=instance.product,
            )

            if CoreTestMpttNode.objects.filter(marketing_plan=instance.product).exists():
                # get the sponsor from the valid input
                sponsor = CoreTestMpttNode.objects.get(
                    user=instance.sponsor, marketing_plan=instance.product)
                allAncestors = sponsor.get_ancestors(
                    include_self=True, ascending=True).order_by('level')
                money = instance.product
                # fare = money.
                allLvl = []
                [allLvl.append({'lvl': x.level, 'usr': str(x.user.user_id)})
                 for x in allAncestors]
                # reverse the list to reverse the levels
                allLvl = allLvl[::-1]
                allDescendants = sponsor.get_descendants()
                allDirect = []
                allDown = []
                # allRanks = []
                [allDirect.append(x) for x in allDescendants if (x.level == 1)]
                [allDown.append(x) for x in allDescendants if (x.level > 1)]
                marketing_setting = CoreMarketingSetting.objects.filter(
                    final=True)

                if not marketing_setting.exists():
                    # default incase of no data
                    pv_etb_rate = 3
                else:
                    pv_etb_rate = marketing_setting[0].pv_rate_etb

                # reward bonus for this specific user
                if instance.product.has_purchase_bonus:
                    userWallet = Marketingwallet.objects.get(
                        user=instance.ordered_by)
                    affWallet = Ewallet.objects.get(
                        user=instance.ordered_by
                    )
                    purchase_bonus = instance.product.purchase_bonus
                    userWallet.amount += pv_etb_rate*purchase_bonus
                    userWallet.pv_count = purchase_bonus
                    affWallet.amount += pv_etb_rate*purchase_bonus
                    affWallet.save()
                    userWallet.save()
                # save all ranks
                # [allRanks.append(rank) for rank in Rank.objects.all()]
                # print(allAncestors, 'ALL ANCESTORS')
                # for ancestor in allAncestors:
                #     print(ancestor.user, "ANCES")
                # for usrs, ranks in zip(allAncestors, allRanks):
                #     # the current affilate
                #     aff = Affilate.objects.get(user=usrs.user)
                #     mWallet = Marketingwallet.objects.get(
                #         user=usrs.user
                #     )
                #     usr_pv = mWallet.pv_count
                #     print("RANKS {}".format(ranks))
                #     print("USERS PV => {}".format(usr_pv))
                #     if (ranks.count_based_on == 'pvval' and usr_pv == ranks.total_pv_count):
                #         print("user is ELLIGIABLE FOR RANK")
                for usrs, x in zip(allAncestors, allLvl):
                    # award pv for all the ancestors above the current user
                    aff = Affilate.objects.get(user=usrs.user)
                    mWallet = Marketingwallet.objects.get(
                        user=usrs.user
                    )
                    affWallet = Ewallet.objects.get(
                        user=usrs.user
                    )
                    fare = money.__dict__[
                        'level{}_percentage'.format(x['lvl']+1)]
                    print(fare, "FAREEE", "{} GIVEN TO {} LEVEL->{}".format(fare,
                                                                            usrs.user, usrs.level+1))
                    affWallet.amount += pv_etb_rate*(money.joining_pv * fare)
                    affWallet.save()
                    mWallet.amount += pv_etb_rate*(money.joining_pv * fare)
                    mWallet.pv_count += money.joining_pv
                    mWallet.save()
                    print(aff, "FARE = {}".format(fare),
                          "AMT {}".format(money.joining_pv))
                    aff.save_mplan_data(
                        len(allDirect), mWallet.amount, len(allDown), money)
                    # grant ranks for those who deserve it
                    print("USER => {} & PV => {}".format(
                        usrs.user, mWallet.pv_count))
                reward_ranks(allAncestors)

                CoreTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=sponsor
                )
            else:
                CoreTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=None
                )
                print("NIBBAA")
                # sponsor = None

            instance.paid_already = True
            instance.save()
