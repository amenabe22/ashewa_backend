from pprint import pprint
from vendors.models import VendorLevelPlans
from core_marketing.models import UnilevelNetwork
from accounts.models import CustomUser, Affilate, CoreLevelPlans


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
        self.setup_plans()
        fin_netpack = []
        for nt in nets:
            if nt['core_level'] == cnt:
                # print(nt['core_level'], cnt)
                fin_netpack.append(nt)
            # else:
            #     raise Exception("Level not reached yet")
        return fin_netpack

    def get_all_nets(self, user: CustomUser):
        # self.setup_plans()
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
