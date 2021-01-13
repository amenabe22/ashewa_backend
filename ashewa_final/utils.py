# helper functions
import math
from accounts.models import Affilate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from vendors.models import VendorLevelPlans
from core_marketing.models import CoreLevelPlans
from core_marketing.models import AffilatePlans
from collections import abc
from django.forms.models import model_to_dict
from pprint import pprint


def recurs_iter(nested):
    for key, value in nested.items():
        if type(value) is list:
            for k, v in nested.items():
                if isinstance(v, list):
                    print(v['children'])
                # if type(v[0]) is dict:
                #     print("NIGGAA")

            # print(value,"HE HE HE HE")
    # for key, value in nested.items():
    #     if isinstance(value, list):
    #         print(next(iter(value)),"SSS")
        # print(isinstance(value, list))
        # print(key, value)
        # print("@"*10)
        # if isinstance(value, dict)
        # if isinstance(value, abc.Mapping):
        #     yield from recurs_iter(value)
        # print(key, value)


def get_orders_paginator(qs, page_size, page, usr, paginated_type, **kwargs):
    p = Paginator(qs, page_size)

    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        print("LL"*20)
        page_obj = p.page(p.num_pages)
    if len(page_obj.object_list) == 0:
        return paginated_type(
            page=page_obj.number,
            pages=p.num_pages,
            total=math.ceil(qs.count()/page_size),
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            objects=[],
            ** kwargs
        )

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        total=math.ceil(qs.count()/page_size),
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def get_core_paginator(qs, page_size, page, usr, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    # print(p.page(page),"!!"*10)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        print("LL"*20)
        page_obj = p.page(p.num_pages)
        # if list(page_obj.object_list[0].__dict__.keys())['']
        module_name = page_obj.object_list[0].__module__
        if module_name == "accounts.models":
            return paginated_type(
                # page=page_obj.number,
                # pages=p.num_pages,
                # total=math.ceil(qs.count()/page_size),
                # has_next=page_obj.has_next(),
                # has_prev=page_obj.has_previous(),
                objects=CoreLevelPlans.objects.none(),
                **kwargs
            )

        if module_name == "vendors.models":
            vend_qs = VendorLevelPlans.objects.none()
            # print(page_obj.object_list[0].core_id , "2"*20)
            return paginated_type(
                # page=page_obj.number,
                # pages=p.num_pages,
                # total=math.ceil(qs.count()/page_size),
                # has_next=page_obj.has_next(),
                # has_prev=page_obj.has_previous(),
                objects=vend_qs,
                **kwargs
            )
    # print(page_obj.object_list, "!"*20)
    if len(page_obj.object_list) == 0:
        return paginated_type(
            page=page_obj.number,
            pages=p.num_pages,
            total=math.ceil(qs.count()/page_size),
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            objects=[],
            ** kwargs
        )
    module_name = page_obj.object_list[0].__module__
    if module_name == "accounts.models":
        plnSet = []
        [plnSet.append({'val': CoreLevelPlans.objects.filter(
            core_id=x.core_id), 'taken': AffilatePlans.objects.filter(
            affilate=Affilate.objects.get(user=usr),
            core_plan=x
        ).exists()
        }) for x in page_obj.object_list]

        return paginated_type(
            page=page_obj.number,
            pages=p.num_pages,
            total=math.ceil(qs.count()/page_size),
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            objects=plnSet,
            ** kwargs
        )
    if module_name == "vendors.models":
        plnSet = []
        [plnSet.append({'val': VendorLevelPlans.objects.filter(
            core_id=x.core_id), 'taken': AffilatePlans.objects.filter(
            affilate=Affilate.objects.get(user=usr),
            vendor_plan=x
        ).exists()
        }) for x in page_obj.object_list]

        return paginated_type(
            page=page_obj.number,
            pages=p.num_pages,
            total=math.ceil(qs.count()/page_size),
            has_next=page_obj.has_next(),
            has_prev=page_obj.has_previous(),
            objects=plnSet,
            **kwargs
        )

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        total=math.ceil(qs.count()/page_size),
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


# def get_tree(affilate):
#     tree = model_to_dict(affilate, fields=['user', 'parent'])
#     if affilate.children.all().exists():
#         children = list()
#         for child in affilate.children.all():
#             children.append(get_tree(child))
#         tree['children'] = children
#     return tree


def get_net_tree(net):
    tree = model_to_dict(net, fields=['affilate', 'user', 'marketing_plan'])
    tree = net.__dict__

    if net.kids.all().exists():
        children = list()
        for child in net.kids.all():
            children.append(get_net_tree(child))
        tree['children'] = children

    return tree


def manage_data(net):
    for idx, x in enumerate(net):
        if 'children' in x.keys():
            manage_data(x['children'])
            for kd in x['children']:
                # print("_"*100)
                plan = CoreLevelPlans.objects.get(
                    core_id=kd['marketing_plan_id'])
                if (idx+1) <= plan.count:
                    affilate = Affilate.objects.get(
                        affilate_id=kd['affilate_id'])
                    print(plan, affilate)

                # print(Affilate.objects.get(affilate_id=kd['affilate_id']))
                # print("_"*100)
            # print("#"*120)
            # print(x['children'])
            # print("#"*120)
        else:
            pass
