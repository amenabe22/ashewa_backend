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
from .utils import get_pv_rate


def core_mail_sender(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, recipient_list)
    print("EMAIL SENT")


def get_updated_aff_data(current_mptt):
    allDownline = current_mptt.get_descendants(include_self=True)
    allDown = []
    allDirect = []
    for des in allDownline:
        if(des == current_mptt):
            allDirect.append(des)
        else:
            allDown.append(des)
    return (len(allDirect), len(allDown))


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
                emailMessage = """Congratulations !!!! \nYou have achieved the Ashewa {} Reward.\nYou can contact us at {} and we will be intouch with you with details of your reward. \n Thanks For working with Ashewa !!!""".format(
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
            newAffPlan = AffilatePlans.objects.create(
                affilate=affilate,
                plan_type='core',
                core_plan=instance.product,
            )
            parent_earning_etb = 0
            parent_earning_pv = 0

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
                pv_etb_rate = get_pv_rate()
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
                    naff = AffilatePlans.objects.get(
                        affilate=affilate,
                        plan_type='core',
                        core_plan=instance.product,
                    )
                    naff.total_earned += pv_etb_rate*purchase_bonus
                    naff.total_earned_pv += purchase_bonus
                    naff.save()
                for usrs, x in zip(allAncestors, allLvl):
                    # award pv for all the ancestors above the current user
                    # get the new updated affilates direct and downline counts
                    all_direct, all_downline = get_updated_aff_data(usrs)
                    print(usrs.user, "<=>"*30)
                    aff = Affilate.objects.get(user=usrs.user)
                    anAfPackage = AffilatePlans.objects.get(
                        affilate=aff,
                        plan_type='core',
                        core_plan=instance.product,
                    )
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
                    anAfPackage.total_earned += pv_etb_rate * \
                        (money.joining_pv * fare)
                    # update directs count
                    anAfPackage.total_direct_referrals = all_direct
                    # update downlines count
                    anAfPackage.total_downline = all_downline
                    # update the earned pv for all the descendants
                    anAfPackage.total_earned_pv += money.joining_pv*fare
                    anAfPackage.save()
                    # if usrs == sponsor:
                    print("_"*40)
                    print("$"*40, "=====", sponsor.user, "@@@@@222@2")
                    # to see how much earned per node old code to be removed
                    # usrs.parent_earning_etb += pv_etb_rate * \
                    #     (money.joining_pv * fare)
                    # usrs.parent_earning_pv += money.joining_pv * fare
                    # usrs.save()
                    print("_"*40)
                    # print(aff, "FARE = {}".format(fare),
                    #       "AMT {}".format(money.joining_pv))
                    aff.save_mplan_data(
                        len(allDirect), mWallet.amount, len(allDown), money)
                    # grant ranks for those who deserve it
                    # print("USER => {} & PV => {}".format(
                    #     usrs.user, mWallet.pv_count))
                reward_ranks(allAncestors)

                CoreTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=sponsor,
                    parent_earning_etb=parent_earning_etb,
                    parent_earning_pv=parent_earning_pv
                )
            else:
                if instance.product.has_purchase_bonus:
                    userWallet = Marketingwallet.objects.get(
                        user=instance.ordered_by)
                    affWallet = Ewallet.objects.get(
                        user=instance.ordered_by
                    )
                    purchase_bonus = instance.product.purchase_bonus
                    userWallet.amount += get_pv_rate() * purchase_bonus
                    userWallet.pv_count = purchase_bonus
                    affWallet.amount += get_pv_rate()*purchase_bonus
                    affWallet.save()
                    userWallet.save()
                    naff = AffilatePlans.objects.get(
                        affilate=affilate,
                        plan_type='core',
                        core_plan=instance.product,
                    )
                    naff.total_earned += get_pv_rate()*purchase_bonus
                    naff.total_earned_pv += purchase_bonus
                    naff.save()
                CoreTestMpttNode.objects.create(
                    user=instance.ordered_by,
                    marketing_plan=instance.product,
                    parent=None
                )
            instance.paid_already = True
            instance.save()
