from pprint import pprint  # for debugging
from core_marketing.models import UnilevelNetwork
from accounts.models import CoreLevelPlans, Affilate
# import sys
# sys.setrecursionlimit(10000)


class MlmNetworkManager(object):
    def __init__(self, plan):
        self.plan = self.get_plan_obj(plan)
        self.all_nets = self.get_all_nets()
        self.user_direct_data = {}

    def get_plan_obj(self, plan):
        return CoreLevelPlans.objects.get(core_id=plan)

    def get_all_nets(self):
        return UnilevelNetwork.objects.filter(marketing_plan=self.plan)

    def read_relation(self):
        for net in self.all_nets:
            father_user = net.affilate.user
            child_user = net.user
            # print("[{}] Brought [{}]".format(father_user, child_user))

    def get_user_relations(self, user):
        # get the affilate
        aff = Affilate.objects.filter(user=user)
        if aff.exists():
            affilate = aff[0]
            # get the specific affilate relations
            usr_direct_relation = UnilevelNetwork.objects.filter(
                marketing_plan=self.plan, affilate=affilate)
            self.user_direct_data.update(
                {'count': usr_direct_relation.count(), 'content': usr_direct_relation, 'children': []})
            for (idx, usrs) in enumerate(self.user_direct_data['content']):
                print(idx, " ==> ", usrs)
                self.get_user_relations(usrs.user)
        # print(self.user_direct_data)

    def get_tree(self, user):
        plan_sets = {'first': [], 'second': [],
                     'third': [], 'fourth': [], 'fivth': [], 'sixth': []}
        affilate = Affilate.objects.filter(user=user)
        if affilate.exists():
            affilate = affilate[0]
        all_affilate_nets = UnilevelNetwork.objects.filter(
            marketing_plan=self.plan, affilate=affilate
        )
        # print(all_affilate_nets,"SSS"*200)
        for af in all_affilate_nets:
            # print(af.user)
            print(af,"LL"*10)
            plan_sets['first'].append({
                'user': af.user,
                # 'level': 1
            })
            print(plan_sets)
        # TODO: what does this do ?
        lstIdxs = list(plan_sets.keys())
        for idx, (mn, sn) in enumerate(zip(lstIdxs, lstIdxs)):
            # print(plan_sets[mn], "{}\n".format(mn))
            for aff in plan_sets[mn]:
                if Affilate.objects.filter(user=aff['user']).exists():
                    nets = UnilevelNetwork.objects.filter(
                        marketing_plan=self.plan, affilate=Affilate.objects.get(
                            user=aff['user']
                        )
                    )
                    for i in nets:
                        plan_sets[sn].append(
                            {'user': i.user, 'level': idx+2}
                        )
        allIdx = []
        for l in range(len(lstIdxs)):
            allIdx.append(l)
        for x in sorted(allIdx, reverse=True):
            [
                plan_sets[lstIdxs[x-1]].append(fin)
                for fin in plan_sets[lstIdxs[x]]
            ]

        return plan_sets

    def form_tree(self, usr):
        tree = self.get_tree(usr)['first']
        for idx, val in enumerate(tree):
            usr_inside_tree = tree[idx]['user']
            print(usr_inside_tree,"SSS\n\n")
            tree[idx]['children'] = self.parse_nets(usr_inside_tree)
            tree[idx]['user'] = tree[idx]['user'].username
        return tree

    def parse_nets(self, user):
        fin = []
        _gen = self.get_tree(user)
        for x in _gen['first']:
            # self.form_tree(x['user'])
            print("X\n", x['user'])
            fin.append({'user': x['user'].username,
                        'children': self.form_tree(x['user']),
                        'core_level': x['level']})

        return fin
        # print(lstIdxs[1:], "LAST INDEXES \n")
        # print("\nDEBUG\n")
        # print(self.plan, "PLAN\n", user)
        # print(plan_sets)
        # print("\nDEBUG\n")
        # print(affilate, "affilate model")
        # print(self.all_nets)
# def do_Stuff():
#     return UnilevelNetwork.objects.all()
