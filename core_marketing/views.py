from pprint import pprint
from django.shortcuts import render
from django.http import JsonResponse
from .core_manager import UniLevelMarketingNetworkManager


def getGen(request, plan):
    network_manager = UniLevelMarketingNetworkManager(
        planid=plan, plan_type="core"
    )
    # network_manager.get_genology()
    # for x in network_manager.planSets['firstSets']:
    #     x['user']
    fin = network_manager.get_all_nets(user=request.user)
    pprint(fin)
    # for x, val in enumerate(fin):
    #     print("@"*20)
    #     if len(val['tree']) > 0:
    #         [print(val['tree'][0][i]) for i in list(val['tree'][0].keys())]
    # [print(i) for i in list(val['tree'][0].keys())]
    # print("@"*20)
    return JsonResponse(fin, safe=False)
