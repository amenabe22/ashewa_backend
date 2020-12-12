# helper functions
import math
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from vendors.models import VendorLevelPlans
from core_marketing.models import CoreLevelPlans


def get_core_paginator(qs, page_size, page, paginated_type, **kwargs):
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
    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        total=math.ceil(qs.count()/page_size),
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )
