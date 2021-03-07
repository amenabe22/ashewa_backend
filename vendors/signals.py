from .models import Order, Vendor
from django.dispatch import receiver
from django.db.models.signals import post_save
from core_marketing.models import(
    Affilate, AffilatePlans, CoreVendorTestMpttNode, CoreVendorMlmOrders, Marketingwallet, Ewallet)


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


@receiver(post_save, sender=Order)
def core_order_approval_handler(sender, instance: Order, **kwargs):
    if not instance.paid_already:
        if instance.order_status == 'cmp':
            print("S"*20)
            print("Order Flagged Completed")
            print("S"*20)
            if instance.product.vendor_plans is not None:
                if instance.product.vendor_plans.creator == instance.ordered_from:
                    print("*"*20)
                    print("Linked Package recognized")
                    print("*"*20)
                    package = instance.product.vendor_plans
                    # check if the one who ordered has the package
                    ordered_by = instance.ordered_by
                    if not Affilate.objects.filter(user=ordered_by):
                        Affilate.objects.create(user=ordered_by)
                    affilate = Affilate.objects.get(user=ordered_by)
                    user_package_ownership_status = AffilatePlans.objects.filter(
                        affilate=affilate, plan_type='ven', vendor_plan=package)
                    affilate_package = None
                    packageData = {'package': affilate_package, 'new': False}
                    # create affilate package for user if it don't already exists
                    if not user_package_ownership_status.exists():
                        packageData['new'] = True
                        packageData['package'] = AffilatePlans.objects.create(
                            affilate=affilate, plan_type='ven', vendor_plan=package)
                        print("user don't have the package already !!!")
                    else:
                        packageData['package'] = user_package_ownership_status[0]
                        packageData['new'] = False

                    # now perform pacakge deduction Logic
                    sponsor = instance.sponsor
                    # chek if sponsor is in the MLm and only if the package is not None
                    if package is not None:
                        sponsor_vmlm = CoreVendorTestMpttNode.objects.filter(
                            user=sponsor, marketing_plan=package)
                        if not sponsor_vmlm.exists():
                            # Just approve the order and stop here as this whole transaction is initial
                            # And the sponsor isn't correct
                            # create the layer
                            CoreVendorTestMpttNode.objects.create(
                                user=ordered_by, marketing_plan=package
                            )
                            print("Sponsor don't have the package")
                        else:
                            allAncestors = sponsor_vmlm[0].get_ancestors(
                                include_self=True, ascending=True).order_by('level')
                            # get the purchase fee
                            money = instance.product.vendor_plans
                            allLvl = []
                            [allLvl.append({'lvl': x.level, 'usr': str(x.user.user_id)})
                             for x in allAncestors]
                            allLvl = allLvl[::-1]
                            allDescendants = sponsor_vmlm[0].get_descendants()
                            allDirect = []
                            allDown = []
                            [allDirect.append(x)
                             for x in allDescendants if (x.level == 1)]
                            [allDown.append(x)
                             for x in allDescendants if (x.level > 1)]
                            # start downline rewards
                            for usrs, x in zip(allAncestors, allLvl):
                                all_direct, all_downline = get_updated_aff_data(
                                    usrs)
                                aff = Affilate.objects.get(user=usrs.user)
                                print(aff, "AFFILATE", money)
                                anAfPackage = AffilatePlans.objects.get(
                                    affilate=aff,
                                    plan_type='ven',
                                    # instance package
                                    vendor_plan=money,
                                )
                                mWallet = Marketingwallet.objects.get(
                                    user=usrs.user
                                )
                                affWallet = Ewallet.objects.get(
                                    user=usrs.user
                                )
                                fare = money.linked_package.repurchase_level.__dict__[
                                    'level{}_percentage'.format(x['lvl']+1)]
                                affWallet.amount += money.purchase_bonus * fare
                                affWallet.save()
                                # add pv if it's necessary at some point if we start giving out for more transactions with vendor packages and affilates
                                mWallet.amount += money.purchase_bonus * fare
                                mWallet.save()
                                # update affilate activity packIage
                                anAfPackage.total_earned += money.purchase_bonus * fare
                                anAfPackage.total_direct_referrals = all_direct
                                anAfPackage.total_downline = all_downline
                                anAfPackage.save()
                                # no need to reward ranks at this point
                                print(fare, "FARE")
                            CoreVendorTestMpttNode.objects.create(
                                user=ordered_by, marketing_plan=package,
                                parent=sponsor_vmlm[0]
                            )
                            # simple test loggers
                            # start giving package based on package level
                        # save and flag it as paid
                        instance.order_stats = 'cmp'
                        instance.paid_already = True
                        instance.save()
