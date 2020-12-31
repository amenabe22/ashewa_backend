import graphql
import graphene
import graphql_jwt
from pprint import pprint
from .utils import get_core_paginator
from .admin_mutations import CreateMarketingPlans
from vendors.models import Vendor, VendorLevelPlans
from core_ecommerce.types import (
    ProductImageType, ProductsType, ParentCategoryType,
    CategoryType, SubCatsType, ProductsPaginatedType)
from vendors.vendor_mutations import UpdateStoreCover
from graphene_django import DjangoObjectType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from accounts.account_mutations import NewUserMutation
from accounts.types import CoreUsersType, UsersDataType
from accounts.models import CustomUser, Affilate
from core_ecommerce.models import(
    Products, ProductImage, ParentCategory, Category, SubCategory)
from .core_perimssions import VendorsPermission, AdminPermission, AffilatePermission
from core_marketing.models import CoreLevelPlans, UnilevelNetwork, AffilatePlans
from vendors.types import VendorType, VendorPlanType, VendorPlanPaginatedType
from core_marketing.types import(LinesDataType,
                                 CoreMarketingPlanTypes, SingleNetworkLayerType, SingleNet, AffilatePlansType, CorePlanPaginatedType)
from core_ecommerce.product_mutations import(
    NewProductMutation, CreateParentCategory, CreateCategory, CreateSubCategory)
from core_marketing.core_manager import UniLevelMarketingNetworkManager
from core_marketing.marketing_mutations import AddPlanMutation, CreateMlmLayer
from .utils import recurs_iter
from core.core_marketing_manager import MlmNetworkManager


class Query(graphene.ObjectType):
    data = graphene.List(VendorType)
    parent_cats = graphene.List(ParentCategoryType)
    cats = graphene.List(CategoryType)
    all_users = graphene.List(CoreUsersType)
    sub_cats = graphene.List(SubCatsType)
    all_marketing_plans = graphene.Field(
        CorePlanPaginatedType, page_size=graphene.Int(), page=graphene.Int())
    any_marketing_plans = graphene.List(CoreMarketingPlanTypes)
    vendor_products = graphene.Field(
        ProductsPaginatedType, page=graphene.Int(), page_size=graphene.Int())
    store_products = graphene.Field(
        ProductsPaginatedType, page=graphene.Int(), page_size=graphene.Int(), store=graphene.String())

    user_data = graphene.List(UsersDataType)
    see_gen = graphene.List(SingleNet,
                            #  SingleNetworkLayerType,
                            plan=graphene.String())
    get_gen = graphene.JSONString(plan=graphene.String())
    all_vendor_plans = graphene.Field(
        VendorPlanPaginatedType, page_size=graphene.Int(), page=graphene.Int())
    all_core_plans = graphene.List(CoreMarketingPlanTypes)
    affilate_plans = graphene.List(AffilatePlansType)
    store_vendor_plan = graphene.List(VendorPlanType)
    store_meta_data = graphene.List(VendorType, store=graphene.String())
    get_lines = graphene.List(LinesDataType, plan=graphene.String())
    get_plan_detail = graphene.List(AffilatePlansType, plan=graphene.String())
    pull_data = graphene.String()
    prod_detail = graphene.Field(ProductsType, product=graphene.String())
    # this is test
    test = graphene.String()

    def resolve_prod_detail(self, info, product):
        return Products.objects.get(product_id=product)

    def resolve_test(self, info):
        man = MlmNetworkManager(plan="8f51d390-0d31-41ba-94ad-1cbda0b09500")
        # man.read_relation()
        _t = man.form_tree(info.context.user)
        print(_t)
        return "Hey this is some test"

    def resolve_pull_data(self, info):
        testAff = Affilate.objects.filter(user=info.context.user)
        plan = CoreLevelPlans.objects.get(
            core_id="8f51d390-0d31-41ba-94ad-1cbda0b09500")
        net = UniLevelMarketingNetworkManager(
            planid="8f51d390-0d31-41ba-94ad-1cbda0b09500", plan_type="core")
        affNet = AffilatePlans.objects.filter(
            affilate=testAff[0], core_plan=plan)
        print(affNet, "HERE")

        # all_n = net.get_all_nets(info.context.user)
        firstLevels = net.get_net_by_lvl(net.parse_nets(info.context.user), 1)
        print(firstLevels, "AGAIN")

        # print(plan.count, "TOTAL SHOULD BE TILL HERE")
        totalDowns = 0
        print(plan, info.context.user, "TEST")
        for i in range(plan.count):
            if i > 1:
                allLens = net.get_net_by_lvl(
                    net.parse_nets(info.context.user), i)
                print()
                print(len(allLens), "@@@", allLens, "==> % d" % i)
                print()
                totalDowns += len(allLens)
        print(affNet, "NNNN"*20)
        print(affNet, "NNNN"*20, totalDowns, len(firstLevels))

        # print(totalDowns,"TOTAL DOWNS")
        affNet.update(total_direct_referrals=len(
            firstLevels), total_downline=totalDowns)
        # print(len(firstLevels))
        # print("#"*10)
        # print()
        # print(len(all_n))
        # print("#"*10)
        # print(all_n, affNet)
        return "HEY THERE"

    @permissions_checker([IsAuthenticated])
    def resolve_get_plan_detail(self, info, plan):
        if not AffilatePlans.objects.filter(
            plan_id=plan
        ).exists():
            raise Exception("Affilate plan not found")
        affplan = AffilatePlans.objects.filter(
            plan_id=plan
        )
        # start of affilateNet data setup
        # print(affplan[0].core_plan.core_id, "PLAN ID")
        # net = UniLevelMarketingNetworkManager(
        #     planid=affplan[0].core_plan.core_id, plan_type="core")
        # affNet = AffilatePlans.objects.filter(
        #     affilate=affplan[0].affilate, core_plan=CoreLevelPlans.objects.get(
        #         core_id=affplan[0].core_plan.core_id
        #     ))
        # firstLevels = net.get_net_by_lvl(net.parse_nets(info.context.user), 1)

        # totalDowns = 0
        # for i in range(affplan[0].core_plan.count):
        #     if i > 1:
        #         allLens = net.get_net_by_lvl(
        #             net.parse_nets(info.context.user), i)
        #         totalDowns += len(allLens)

        # affNet.update(total_direct_referrals=len(
        #     firstLevels), total_downline=totalDowns)
        # end of affilateNet data setup
        return affplan
        # here is where the plans data is rendered

    def resolve_store_meta_data(self, info, store):
        return Vendor.objects.filter(vendor_id=store)

    @permissions_checker([VendorsPermission])
    def resolve_store_vendor_plan(self, info):
        return VendorLevelPlans.objects.filter(
            creator=Vendor.objects.get(
                user=info.context.user
            )
        )

    @permissions_checker([AffilatePermission])
    def resolve_affilate_plans(self, info):
        return AffilatePlans.objects.filter(
            affilate=Affilate.objects.get(user=info.context.user)
        )

    @permissions_checker([IsAuthenticated])
    def resolve_all_core_plans(self, info):
        return CoreLevelPlans.objects.all()

    @permissions_checker([VendorsPermission, IsAuthenticated])
    def resolve_vendor_products(self, info, page, page_size):
        qs = Products.objects.filter(
            vendor=Vendor.objects.get(
                user=info.context.user
            )).order_by('-created_timestamp')

        return get_core_paginator(qs, page_size, page, None, ProductsPaginatedType)

    # @permissions_checker([VendorsPermission, IsAuthenticated])
    def resolve_store_products(self, info, page, page_size, store):
        qs = Products.objects.filter(
            vendor=Vendor.objects.get(vendor_id=store
                                      )).order_by('-created_timestamp')

        return get_core_paginator(qs, page_size, page, None, ProductsPaginatedType)

    @permissions_checker([IsAuthenticated])
    def resolve_all_vendor_plans(self, info, page_size, page):
        qs = VendorLevelPlans.objects.all()
        return get_core_paginator(qs, page_size, page, info.context.user, VendorPlanPaginatedType)
        # return VendorLevelPlans.objects.all()

    @permissions_checker([AffilatePermission])
    def resolve_get_gen(self, info, plan):
        network_manager = UniLevelMarketingNetworkManager(
            planid=plan, plan_type="core"
        )
        # network_manager.get_genology()
        # for x in network_manager.planSets['firstSets']:
        #     x['user']
        fin = network_manager.get_all_nets(user=info.context.user)
        return fin

    @permissions_checker([AffilatePermission])
    def resolve_see_gen(self, info, plan):
        network_manager = UniLevelMarketingNetworkManager(
            planid=plan, plan_type="core"
        )
        fin = network_manager.get_all_nets(user=info.context.user)
        return fin

    @permissions_checker([IsAuthenticated])
    def resolve_layers_data(self, info):
        return UnilevelNetwork.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_user_data(self, info):
        print(info.context.user)
        return CustomUser.objects.filter(
            user_id=info.context.user.user_id)

    @permissions_checker([AffilatePermission])
    def resolve_all_marketing_plans(self, info, page_size, page):
        qs = CoreLevelPlans.objects.all()
        # aff = Affilate.objects.get(user=info.context.user)
        print("#"*30)
        return get_core_paginator(qs,
                                  page_size, page,
                                  info.context.user,
                                  CorePlanPaginatedType)

    @permissions_checker([IsAuthenticated])
    def resolve_any_marketing_plans(self, info):
        qs = CoreLevelPlans.objects.all()
        # aff = Affilate.objects.get(user=info.context.user)
        return qs
        # return get_core_paginator(qs,
        #                           page_size, page,
        #                           info.context.user,
        #                           CorePlanPaginatedType)

    @permissions_checker([AdminPermission])
    def resolve_all_users(self, info):
        return CustomUser.objects.all()

    def resolve_parent_cats(self, info):
        return ParentCategory.objects.all()

    def resolve_cats(self, info):
        return Category.objects.all()

    def resolve_sub_cats(self, info):
        return SubCategory.objects.all()

    @permissions_checker([VendorsPermission])
    def resolve_data(self, info):
        return Vendor.objects.filter(user=info.context.user)

    @permissions_checker([AffilatePermission])
    def resolve_get_lines(self, info, plan):
        network_manager = UniLevelMarketingNetworkManager(
            planid=plan, plan_type="core"
        )
        fin = network_manager.get_all_nets(user=info.context.user)
        for x in fin:
            p = recurs_iter(x)
        return [{'name': 'Dowline', 'value': 'value'}]


class Mutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_mplan = CreateMarketingPlans.Field(
        description="create marketing plans")
    add_product = NewProductMutation.Field(description="add new product")
    create_parent_cat = CreateParentCategory.Field(
        description="create parent category")
    create_cat = CreateCategory.Field(description="create category")
    create_scat = CreateSubCategory.Field(description="create sub category")
    update_store_pic = UpdateStoreCover.Field(description="Update store cover")
    new_user = NewUserMutation.Field(description="create new user")
    add_plan_mutation = AddPlanMutation.Field(
        description="add a plan for an affilate")
    create_mlm_layer = CreateMlmLayer.Field(
        description="Create a new core mlm layer"
    )


schema = graphene.Schema(query=Query, mutation=Mutations)
