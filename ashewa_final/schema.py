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
from core_marketing.marketing_mutations import AddPlanMutation
from .utils import recurs_iter


class Query(graphene.ObjectType):
    data = graphene.List(VendorType)
    parent_cats = graphene.List(ParentCategoryType)
    cats = graphene.List(CategoryType)
    all_users = graphene.List(CoreUsersType)
    sub_cats = graphene.List(SubCatsType)
    all_marketing_plans = graphene.Field(
        CorePlanPaginatedType, page_size=graphene.Int(), page=graphene.Int())
    vendor_products = graphene.Field(
        ProductsPaginatedType, page=graphene.Int(), page_size=graphene.Int())
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

    @permissions_checker([VendorsPermission])
    def resolve_vendor_products(self, info, page, page_size):
        qs = Products.objects.filter(
            vendor=Vendor.objects.get(
                user=info.context.user
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


schema = graphene.Schema(query=Query, mutation=Mutations)
