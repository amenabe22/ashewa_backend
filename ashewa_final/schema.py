import graphql
import graphene
import graphql_jwt
from pprint import pprint
from vendors.types import VendorType
from vendors.models import Vendor
from .utils import get_core_paginator
from .admin_mutations import CreateMarketingPlans
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
from core_marketing.models import CoreLevelPlans, UnilevelNetwork
from core_marketing.types import CoreMarketingPlanTypes, SingleNetworkLayerType
from core_ecommerce.product_mutations import NewProductMutation, CreateParentCategory, CreateCategory, CreateSubCategory
from core_marketing.core_manager import UniLevelMarketingNetworkManager


class Query(graphene.ObjectType):
    data = graphene.List(VendorType)
    parent_cats = graphene.List(ParentCategoryType)
    cats = graphene.List(CategoryType)
    all_users = graphene.List(CoreUsersType)
    sub_cats = graphene.List(SubCatsType)
    all_marketing_plans = graphene.List(CoreMarketingPlanTypes)
    vendor_products = graphene.Field(
        ProductsPaginatedType, page=graphene.Int(), page_size=graphene.Int())
    user_data = graphene.List(UsersDataType)
    see_gen = graphene.List(SingleNetworkLayerType, plan=graphene.String())

    @permissions_checker([AdminPermission])
    def resolve_see_gen(self, info, plan):
        # users network manager library to determine genology tree
        network_manager = UniLevelMarketingNetworkManager(
            plan=plan, user=info.context.user, plan_type="core"
        )
        network_manager.get_genology()
        return network_manager.planSets['firstSets']

    @permissions_checker([IsAuthenticated])
    def resolve_layers_data(self, info):
        return UnilevelNetwork.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_user_data(self, info):
        print(info.context.user)
        return CustomUser.objects.filter(
            user_id=info.context.user.user_id)

    @permissions_checker([AdminPermission])
    def resolve_all_marketing_plans(self, info):
        return CoreLevelPlans.objects.all()

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
    def resolve_vendor_products(self, info, page, page_size):
        qs = Products.objects.filter(
            vendor=Vendor.objects.get(
                user=info.context.user
            )).order_by('-created_timestamp')
        return get_core_paginator(qs, page_size, page, ProductsPaginatedType)

    @permissions_checker([VendorsPermission])
    def resolve_data(self, info):
        return Vendor.objects.filter(user=info.context.user)


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


schema = graphene.Schema(query=Query, mutation=Mutations)
