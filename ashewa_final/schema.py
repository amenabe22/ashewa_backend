import graphql
import graphene
import graphql_jwt
from pprint import pprint
from .admin_mutations import CreateMarketingPlans
from core_ecommerce.types import (LandingCarsType, LandingCatBlockType, UsrOrderType,
                                  ProductImageType, ProductsType, ParentCategoryType,
                                  CategoryType, SubCatsType, ProductsPaginatedType)
from vendors.vendor_mutations import UpdateStoreCover, CreateOrder, LoadCart, PopCart
from graphene_django import DjangoObjectType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from accounts.account_mutations import NewUserMutation
from accounts.types import CoreUsersType, UsersDataType
from accounts.models import CustomUser, Affilate
from core_ecommerce.models import(LandingCarousel,
                                  Products, ProductImage, ParentCategory, Category, SubCategory)
from .core_perimssions import VendorsPermission, AdminPermission, AffilatePermission
from core_marketing.models import (CoreLevelPlans, UnilevelNetwork, AffilatePlans,
                                   TestNetwork, UserMessages, CoreDocs, CoreTestMpttNode, Marketingwallet, CoreMlmOrders)
from vendors.types import(VendorType, VendorPlanType, VendorPlanPaginatedType, VendorOverviewDataType,
                          OrdersType, OrdersPaginatedType, CartsType, CartPaginatedType, VenodrGalleryType)
from vendors.models import Vendor, VendorLevelPlans, Order, Cart, VenodrGallery
from core_marketing.types import(LinesDataType, CoreVendDataType, UserMessagesTyoe, CoreDocsType,
                                 CoreMarketingPlanTypes, SingleNetworkLayerType, SingleNet, AffilatePlansType, CorePlanPaginatedType)
from core_ecommerce.product_mutations import(EditProduct,
                                             NewProductMutation, CreateParentCategory, CreateCategory, CreateSubCategory)
from core_marketing.core_manager import UniLevelMarketingNetworkManager
from core_marketing.marketing_mutations import (AddPlanMutation, CreateMlmLayer, CreateTestLayer, CreateGenv2, CreateCoreMlmOrder, CreateVendorPackage,EditVendorLevelPackage)
from .utils import recurs_iter, get_orders_paginator, get_core_paginator, get_net_tree, manage_data
from core.core_marketing_manager import MlmNetworkManager
from django.forms.models import model_to_dict
from django.db.models import Count
from django.db.models.functions import ExtractDay

# rushed to doing this


class CreateUserMessage(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        full_name = graphene.String()
        email = graphene.String()
        message = graphene.String()

    def mutate(self, info, full_name, email, message):
        try:
            UserMessages.objects.create(
                full_name=full_name, email=email, message=message
            )
        except Exception as e:
            raise Exception(str(e))
        return CreateUserMessage(payload=True)


class Query(graphene.ObjectType):
    venodr_gallery = graphene.List(VenodrGalleryType, store=graphene.String())
    all_products = graphene.Field(
        ProductsPaginatedType, page_size=graphene.Int(), page=graphene.Int())
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
    get_vendor_orders = graphene.Field(
        OrdersPaginatedType, page_size=graphene.Int(), page=graphene.Int())
    get_carts = graphene.Field(
        CartPaginatedType, page_size=graphene.Int(), page=graphene.Int())
    vendor_data = graphene.List(VendorOverviewDataType)

    parse_tree = graphene.String(net=graphene.String())
    core_vend_data = graphene.List(
        CoreVendDataType, year=graphene.Int(), month=graphene.Int())
    landing_cars = graphene.List(LandingCarsType)
    landing_cat_block = graphene.List(
        LandingCatBlockType, count=graphene.Int())
    prod_search = graphene.List(ProductsType, query=graphene.String())
    filter_prods = graphene.Field(ProductsPaginatedType, pcat=graphene.String(
    ), page=graphene.Int(), page_size=graphene.Int(), ranged=graphene.Boolean(), minP=graphene.Int(), maxP=graphene.Int())
    # please delete me
    get_core_docs = graphene.List(CoreDocsType)
    test_me = graphene.String()
    get_genv2 = graphene.JSONString(plan=graphene.String())
    user_orders = graphene.List(UsrOrderType)
    vendor_package_detail = graphene.Field(
        VendorPlanType, plan=graphene.String())

    @permissions_checker([IsAuthenticated])
    def resolve_vendor_package_detail(self, info, plan):
        return VendorLevelPlans.objects.get(core_id=plan)

    @permissions_checker([IsAuthenticated])
    def resolve_user_orders(self, info):
        usr = info.context.user
        _vend_ords = Order.objects.filter(ordered_by=usr)
        _mlm_ords = CoreMlmOrders.objects.filter(ordered_by=usr)
        return [{'ords': _vend_ords, 'core_ord': _mlm_ords}]

    @permissions_checker([IsAuthenticated])
    def resolve_get_genv2(self, info, plan):
        aff = AffilatePlans.objects.get(plan_id=plan)
        # core_plan = CoreLevelPlans(core_id=plan)
        core_plan = aff.core_plan
        print("DEBUG")
        print(aff.core_plan.plan_name)
        userMptt = CoreTestMpttNode.objects.get(marketing_plan=core_plan,
                                                user=CustomUser.objects.get(username=info.context.user))
        allAncestors = userMptt.get_ancestors()
        allDownline = userMptt.get_descendants()
        allDown = []
        allDirect = []
        print("DEBUG")
        mWallet = Marketingwallet.objects.get(user=info.context.user).amount
        [allDown.append(x) for x in allDownline if (x.level > 1)]
        [allDirect.append(x) for x in allDownline if (x.level == 1)]
        finData = {'total_earned': mWallet, 'total_downlines': len(
            allDown), 'total_direct': len(allDirect), 'plan_name': core_plan.plan_name}
        # print("ALL DLINE {}".format(len(allDown)))
        # print("DEBUG")
        return finData

    def resolve_test_me(self, info):
        # first = CoreTestMpttNode.objects._mptt_filter(
        #     user=info.context.user)
        # get ancestors of this specific user
        # print(first.get_ancestors(include_self=True))
        # usrs = []
        # for x in first.get_descendants(): usrs.append(x.user)
        # print(usrs)
        # rln = CoreTestMpttNode.objects._mptt_filter(level__lte=1)
        # [print(x.user, x.level) for x in rln]
        print(CoreTestMpttNode.objects.get(marketing_plan=CoreLevelPlans(core_id="eb1b5ee2-f45b-4723-b595-4ef12176671f"),
                                           user=CustomUser.objects.get(username=info.context.user)).level)
        # [print(x.level) for x in CoreTestMpttNode.objects.all()]
        # level__lte
        # print(first.get_ancestors(include_self=True))
        # print(CoreTestMpttNode.objects.tree_model())
        return "Hey there"

    def resolve_get_core_docs(self, info):
        return CoreDocs.objects.all()

    def resolve_venodr_gallery(self, info, store):
        return Vendor.objects.get(vendor_id=store).store_gallery.all()

    def resolve_filter_prods(self, info, pcat, page_size, page, minP, maxP, ranged):
        if pcat is not None:
            try:
                # check ranged status
                if ranged:
                    qs = Products.objects.filter(product_parent_category=ParentCategory.objects.get(
                        pcat_id=pcat, selling_price__range=(minP, maxP),
                    )).order_by('-created_timestamp')
                else:
                    # return cat filtered if not ranged
                    qs = Products.objects.filter(product_parent_category=ParentCategory.objects.get(
                        pcat_id=pcat,
                    )).order_by('-created_timestamp')
            except Exception as e:
                qs = Products.objects.all().order_by('-created_timestamp')
        else:
            qs = Products.objects.all().order_by('-created_timestamp')

        return get_core_paginator(qs, page_size, page, None, ProductsPaginatedType)

    def resolve_prod_search(self, info, query):
        return Products.objects.filter(product_name__contains=query)

    def resolve_landing_cat_block(self, info, count):
        fin = []
        all_pcats = []
        pcatSet = [{'pcat': None, 'pcatProds': []}]
        allPcats = ParentCategory.objects.all()
        if not(allPcats.count() > 0):
            raise Exception("not pcats registered")
        if count > allPcats.count():
            all_pcats = allPcats[:count]
        else:
            all_pcats = allPcats.order_by(
                '-created_timestamp')[:count]
            print(all_pcats)
            print("@"*30, count)

        for pcs in all_pcats:
            # filter products per that specific category
            pcProds = Products.objects.filter(
                product_parent_category=pcs
            )[:6]
            fin.append({'pcat': pcs, 'catProds': pcProds})

        return fin

    def resolve_landing_cars(self, info):
        return LandingCarousel.objects.all()

    def resolve_all_products(self, info, page_size, page):
        qs = Products.objects.all().order_by('-created_timestamp')

        return get_core_paginator(qs, page_size, page, None, ProductsPaginatedType)

    @ permissions_checker([IsAuthenticated])
    def resolve_core_vend_data(self, info, year, month):
        vend = Vendor.objects.filter(user=info.context.user)
        # print(vend)
        totalSold = Order.objects.filter(
            ordered_from=vend[0], order_status='cmp')
        tq = totalSold.filter(timestamp__year=year,
                              timestamp__month=month
                              ).annotate(
            day=ExtractDay('timestamp'),
        ).values(
            'day'
        ).annotate(
            n=Count('pk')
        ).order_by('day')
        print(tq)
        return tq

    def resolve_parse_tree(self, info, net):
        net = TestNetwork.objects.filter(layer_id=net)
        # tree = get_net_tree(net)
        # print("@"*20)
        # print(net, "FO REAL")
        # print(tree)
        final_tree = list()
        # TODO Why we checking for null main
        # for tst in TestNetwork.objects.filter(parent__isnull=True):
        for tst in net:
            final_tree.append(get_net_tree(tst))
        # pprint(final_tree)
        print("@"*20)
        # manage_data(final_tree)
        print("@"*20)
        # print("@"*20)
        return "runnning tests in the BG"

    @ permissions_checker([IsAuthenticated, VendorsPermission])
    def resolve_vendor_data(self, info):
        allSold = []
        vendor = Vendor.objects.get(user=info.context.user)
        orders = Order.objects.filter(
            ordered_from=vendor, order_status='cmp')
        [allSold.append(order.product.selling_price) for order in orders]
        return [
            {'label': 'Total Sold',
             'val': sum(allSold), }, {'label': 'Total Products', 'val': Products.objects.filter(
                 vendor=vendor
             ).count()}]

    @ permissions_checker([IsAuthenticated])
    def resolve_get_carts(self, info, page, page_size):
        qs = Cart.objects.filter(user=info.context.user).order_by('-timestamp')
        return get_orders_paginator(qs, page_size, page, None, CartPaginatedType)

    @ permissions_checker([VendorsPermission, IsAuthenticated])
    def resolve_get_vendor_orders(self, info, page, page_size):
        qs = Order.objects.filter(ordered_from=Vendor.objects.get(
            user=info.context.user
        )).order_by('-timestamp')

        return get_orders_paginator(qs, page_size, page, None, OrdersPaginatedType)

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

    @ permissions_checker([IsAuthenticated])
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

    @ permissions_checker([VendorsPermission])
    def resolve_store_vendor_plan(self, info):
        return VendorLevelPlans.objects.filter(
            creator=Vendor.objects.get(
                user=info.context.user
            )
        )

    @ permissions_checker([AffilatePermission])
    def resolve_affilate_plans(self, info):
        return AffilatePlans.objects.filter(
            affilate=Affilate.objects.get(user=info.context.user)
        )

    @ permissions_checker([IsAuthenticated])
    def resolve_all_core_plans(self, info):
        return CoreLevelPlans.objects.all()

    @ permissions_checker([VendorsPermission, IsAuthenticated])
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

    @ permissions_checker([IsAuthenticated])
    def resolve_all_vendor_plans(self, info, page_size, page):
        qs = VendorLevelPlans.objects.all()
        return get_core_paginator(qs, page_size, page, info.context.user, VendorPlanPaginatedType)
        # return VendorLevelPlans.objects.all()

    @ permissions_checker([AffilatePermission])
    def resolve_get_gen(self, info, plan):
        network_manager = UniLevelMarketingNetworkManager(
            planid=plan, plan_type="core"
        )
        # network_manager.get_genology()
        # for x in network_manager.planSets['firstSets']:
        #     x['user']
        fin = network_manager.get_all_nets(user=info.context.user)
        return fin

    @ permissions_checker([AffilatePermission])
    def resolve_see_gen(self, info, plan):
        network_manager = UniLevelMarketingNetworkManager(
            planid=plan, plan_type="core"
        )
        fin = network_manager.get_all_nets(user=info.context.user)
        return fin

    @ permissions_checker([IsAuthenticated])
    def resolve_layers_data(self, info):
        return UnilevelNetwork.objects.all()

    @ permissions_checker([IsAuthenticated])
    def resolve_user_data(self, info):
        print(info.context.user)
        return CustomUser.objects.filter(
            user_id=info.context.user.user_id)

    @ permissions_checker([AffilatePermission])
    def resolve_all_marketing_plans(self, info, page_size, page):
        qs = CoreLevelPlans.objects.all()
        # aff = Affilate.objects.get(user=info.context.user)
        print("#"*30)
        return get_core_paginator(qs,
                                  page_size, page,
                                  info.context.user,
                                  CorePlanPaginatedType)

    @ permissions_checker([IsAuthenticated])
    def resolve_any_marketing_plans(self, info):
        qs = CoreLevelPlans.objects.all()
        # aff = Affilate.objects.get(user=info.context.user)
        return qs
        # return get_core_paginator(qs,
        #                           page_size, page,
        #                           info.context.user,
        #                           CorePlanPaginatedType)

    @ permissions_checker([AdminPermission])
    def resolve_all_users(self, info):
        return CustomUser.objects.all()

    def resolve_parent_cats(self, info):
        return ParentCategory.objects.all()

    def resolve_cats(self, info):
        return Category.objects.all()

    def resolve_sub_cats(self, info):
        return SubCategory.objects.all()

    @ permissions_checker([VendorsPermission])
    def resolve_data(self, info):
        return Vendor.objects.filter(user=info.context.user)

    @ permissions_checker([AffilatePermission])
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
    create_order = CreateOrder.Field(
        description="Create new order from any vendor product"
    )
    load_cart = LoadCart.Field(
        description="Load products to cart"
    )
    pop_cart = PopCart.Field(
        description="Delete cart"
    )
    # Create test layer
    create_tlayer = CreateTestLayer.Field()
    user_message = CreateUserMessage.Field(
        description="User Message about coming soon page ..."
    )
    # create genv2
    create_genv2 = CreateGenv2.Field(description="create generation for the ")
    create_cmlm_order = CreateCoreMlmOrder.Field(
        description="create core mlm initial order")

    edit_product = EditProduct.Field(
        description="Edit Products"
    )
    # vendor package CRUDS
    create_vendor_package = CreateVendorPackage.Field(
        description="Create package for vendors"
    )
    edit_vpack = EditVendorLevelPackage.Field(
        description="Edit Vendor Level Package"
    )

schema = graphene.Schema(query=Query, mutation=Mutations)
