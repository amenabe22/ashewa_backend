from pprint import pprint
from vendors.models import VendorLevelPlans
from core_marketing.models import UnilevelNetwork
from accounts.models import CustomUser, Affilate, CoreLevelPlans


class UniLevelMarketingNetworkManager(object):
    def __init__(self, plan, user: CustomUser, plan_type="core"):
        self.plan = plan
        self.user = user
        self.planSets = {}
        self.plan_type = plan_type
        self.affilate = None

    def setup_plans(self):
        try:
            # get the selected marketing plan
            if self.plan_type == "core":
                self.plan = CoreLevelPlans.objects.get(
                    core_id=self.plan
                )
            elif self.plan_type == "vendor":
                self.plan = VendorLevelPlans.objects.get(
                    core_id=self.plan
                )
            else:
                raise Exception("Plan type not found")

        except:
            raise Exception("plan not found")

    def get_genology(self):
        self.setup_plans()
        self.planSets = {'firstSets': [], 'secondSets': [], 'thirdSets': [],
                         'fourth': [], 'fivth': [], 'sixth': []}
        self.affilate = Affilate.objects.get(
            user=self.user
        )
        # start

        curr_affilate = self.affilate
        all_aff_nets = UnilevelNetwork.objects.filter(
            marketing_plan=self.plan, affilate=curr_affilate)

        for x in all_aff_nets:
            self.planSets['firstSets'].append({'user': CustomUser.objects.filter(
                user_id=x.user.user_id), 'level': 1})

        lstIdxs = list(self.planSets.keys())
        for idx, (mn, sn) in enumerate(zip(lstIdxs, lstIdxs[1:])):
            for x in self.planSets[mn]:
                if Affilate.objects.filter(user=x[list(x.keys())[0]][0]).exists():
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
            [self.planSets[lstIdxs[x-1]].append(fin) for fin in self.planSets[lstIdxs[x]]]

        # end
        # allIdx = []
        # for l in range(len(lstIdxs)):
        #     allIdx.append(l)
        # for x in sorted(allIdx, reverse=True):
        #     [self.planSets[lstIdxs[x-1]].append(fin)
        #      for fin in self.planSets[lstIdxs[x]]]

        # for x in sorted(allIdx, reverse=True):
        #     # print("{} ?==? {}".format(lstIdxs[x], lstIdxs[x-1]))
        #     [self.planSets[lstIdxs[x-1]].append(fin)
        #      for fin in self.planSets[lstIdxs[x]]]

        # for idx, (mn, sn) in enumerate(zip(lstIdxs, lstIdxs[1:])):
        #     # print(self.planSets[lstIdxs[x]])
        #     [self.planSets[lstIdxs[idx]].append(x) for x in self.planSets[lstIdxs[idx-1]]]
            # [self.planSets[lstIdxs[x]].append(x)
            #  for x in self.planSets[
            #     lstIdxs[x-1]]]
        return self.planSets
# def resolve_see_gen(self, info, plan):
#     allSets = {'firstSets': [], 'secondSets': [], 'thirdSets': [],
#                'fourth': [], 'fivth': [], 'sixth': []}

#     # get the selected marketing plan
#     _pl = CoreLevelPlans.objects.get(core_id=plan)
#     # get current affilate
#     curr_affilate = Affilate.objects.get(user=info.context.user)
#     # get all nets under the current affilate 1st level
#     all_aff_nets = UnilevelNetwork.objects.filter(
#         marketing_plan=_pl, affilate=curr_affilate)
#     # get all networks under this plan
#     # all_plan_nets = UnilevelNetwork.objects.filter(marketing_plan=_pl)

#     for x in all_aff_nets:
#         allSets['firstSets'].append({'user': CustomUser.objects.filter(
#             user_id=x.user.user_id), 'level': 1})

#     lstIdxs = list(allSets.keys())
#     for idx, (mn, sn) in enumerate(zip(lstIdxs, lstIdxs[1:])):
#         for x in allSets[mn]:
#             if Affilate.objects.filter(user=x[list(x.keys())[0]][0]).exists():
#                 nets = UnilevelNetwork.objects.filter(marketing_plan=_pl,
#                                                       affilate=Affilate.objects.get(
#                                                           user=x['user'][0]))
#                 for i in nets:
#                     allSets[sn].append({'user': CustomUser.objects.filter(
#                         user_id=i.user.user_id
#                     ), 'level': idx+2})
#     allIdx = []
#     for l in range(len(lstIdxs)):
#         allIdx.append(l)
#     for x in sorted(allIdx, reverse=True):
#         # print("{} ?==? {}".format(lstIdxs[x], lstIdxs[x-1]))
#         [allSets[lstIdxs[x-1]].append(fin) for fin in allSets[lstIdxs[x]]]
