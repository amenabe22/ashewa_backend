import re
import graphene
from .types import AffilatePlansType
from vendors.types import VendorPlanType, VendorType
from accounts.models import Affilate, CoreLevelPlans
from django_graphene_permissions import permissions_checker
from .models import AffilatePlans, UnilevelNetwork
from vendors.models import VendorLevelPlans, Vendor, Cart
from ashewa_final.core_perimssions import AffilatePermission
from django_graphene_permissions.permissions import IsAuthenticated
from accounts.models import CustomUser
from ashewa_final.core_perimssions import VendorsPermission
# from core_perimssions import VendorsPermission, AffilatePermission
from core_marketing.models import TestNetwork, CoreTestMpttNode, CoreLevelPlans, CoreMlmOrders, CoreVendorMlmOrders, BillingInfo, CoreVendorTestMpttNode
from core_marketing.types import CoreTestMpttType, CoreMlmOrderType, CoreVendorMlmOrderType
from core_ecommerce.models import PaymentType
UUID_PATTERN = re.compile(
    r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


class EmptyCart(graphene.Mutation):
    payload = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info):
        usrCart = Cart.objects.filter(user=info.context.user)
        usrCart.delete()
        return EmptyCart(payload=True)


class EditVendorLevelPackage(graphene.Mutation):
    payload = graphene.Field(VendorPlanType)

    class Arguments:
        plan_name = graphene.String()
        plan_desc = graphene.String()
        purchase_bonus = graphene.Float()
        plan = graphene.String()
        linked_package = graphene.String()

    @permissions_checker([VendorsPermission, IsAuthenticated])
    def mutate(self, info, plan_name, plan_desc, purchase_bonus, plan, linked_package):
        vendor = Vendor.objects.get(user=info.context.user)
        linkedSet = CoreLevelPlans.objects.filter(core_id=linked_package)
        if not linkedSet.exists():
            raise Exception("package not found")
        try:
            plan = VendorLevelPlans.objects.filter(
                core_id=plan, creator=vendor)
            plan.update(plan_name=plan_name, plan_description=plan_desc, purchase_bonus=purchase_bonus,
                        linked_package=linkedSet[0]
                        )
            # plan = VendorLevelPlans.objects.create(
            #     creator=vendor, plan_name=plan_name, plan_description=plan_desc,
            #     level1_percentage=level_1, level2_percentage=level_2, level3_percentage=level_3,
            #     level4_percentage=level_4, purchase_bonus=purchase_bonus
            # )
        except Exception as e:
            raise Exception(str(e))
        return EditVendorLevelPackage(payload=plan[0])


class CreateVendorPackage(graphene.Mutation):
    payload = graphene.Field(VendorPlanType)

    class Arguments:
        plan_name = graphene.String()
        plan_desc = graphene.String()
        purchase_bonus = graphene.Float()
        linked_package = graphene.String()

    @permissions_checker([VendorsPermission, IsAuthenticated])
    def mutate(self, info, plan_name, plan_desc, purchase_bonus, linked_package):
        vendor = Vendor.objects.get(user=info.context.user)
        package_set = CoreLevelPlans.objects.filter(core_id=linked_package)
        if not package_set.exists():
            raise Exception("package not found")
        try:
            plan = VendorLevelPlans.objects.create(
                creator=vendor, plan_name=plan_name, plan_description=plan_desc,
                purchase_bonus=purchase_bonus, linked_package=package_set[0]
            )
        except Exception as e:
            raise Exception(str(e))
        return CreateVendorPackage(payload=plan)


class CreateVendorPackageOrder(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        full_name = graphene.String()
        address = graphene.String()
        phone = graphene.String()
        mlm = graphene.String()
        sponsor = graphene.String()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, full_name, address, phone, mlm, sponsor):
        binfo = BillingInfo.objects.create(
            full_name=full_name, address=address, phone=phone
        )
        vend_plan = VendorLevelPlans.objects.get(core_id=mlm)
        if(sponsor == str(info.context.user.user_id)):
            raise Exception("User can't be a sponsor")
        if CoreVendorMlmOrders.objects.filter(ordered_by=info.context.user, product=vend_plan).exists():
            raise Exception("Package is already purchased")
        sponsor_user = CustomUser.objects.get(user_id=sponsor)
        if not CoreVendorTestMpttNode.objects.filter(user=CustomUser.objects.get(user_id=sponsor), marketing_plan=vend_plan).exists():
            if not CoreVendorTestMpttNode.objects.filter(marketing_plan=vend_plan, parent=None).exists():
                # this is the first ancestor
                pass
                # parent = CoreTestMpttNode.objects.get(
                #     marketing_plan=core_plan, parent=None)
                # if CoreTestMpttNode.objects.filter(marketing_plan=core_plan, user=info.context.user, parent=parent).exists():
                #     raise Exception("Layer already exists")
            else:
                raise Exception("Invalid sponsor selected")
        if CoreVendorTestMpttNode.objects.filter(
                user=sponsor_user).exists():
            parent = CoreVendorTestMpttNode.objects.get(
                user=sponsor_user, marketing_plan=vend_plan)
            # print(core_plan, info.context.user, CoreTestMpttNode.objects.filter(user=sponsor_user, marketing_plan=core_plan), "SSSSSSSS")
            if CoreVendorTestMpttNode.objects.filter(marketing_plan=vend_plan, user=info.context.user, parent=parent).exists():
                raise Exception("Layer already exists")
        # create the order now
        CoreVendorMlmOrders.objects.create(
            billing_info=binfo, product=vend_plan,
            ordered_by=info.context.user, sponsor=CustomUser.objects.get(
                user_id=sponsor
            ))

        return CreateVendorPackageOrder(payload=True)


class CreateCoreMlmOrder(graphene.Mutation):
    # core mlm order for default packages provided by the company
    payload = graphene.Boolean()

    class Arguments:
        full_name = graphene.String()
        address = graphene.String()
        phone = graphene.String()
        mlm = graphene.String()
        sponsor = graphene.String()
        payment_type = graphene.String()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, full_name, address, phone, mlm, sponsor, payment_type):
        binfo = BillingInfo.objects.create(
            full_name=full_name, address=address, phone=phone
        )

        print(CoreLevelPlans.objects.all())
        core_plan = CoreLevelPlans.objects.get(core_id=mlm)
        print("A"*20, mlm)
        if(sponsor == str(info.context.user.user_id)):
            raise Exception("User can't be a sponsor")

        # check if the layer exists
        if CoreMlmOrders.objects.filter(ordered_by=info.context.user, product=core_plan).exists():
            raise Exception("Plan is already purchased")

        sponsor_user = CustomUser.objects.get(user_id=sponsor)
        # check if the order is being sent by the wrong sponsor
        if not CoreTestMpttNode.objects.filter(user=CustomUser.objects.get(user_id=sponsor), marketing_plan=core_plan).exists():
            if not CoreTestMpttNode.objects.filter(marketing_plan=core_plan, parent=None).exists():
                # this is the first ancestor
                pass
            else:
                raise Exception("Invalid sponsor selected")
        if CoreTestMpttNode.objects.filter(marketing_plan=core_plan):
            if CoreTestMpttNode.objects.filter(
                    user=sponsor_user).exists():
                parent = CoreTestMpttNode.objects.filter(
                    user=sponsor_user, marketing_plan=core_plan)
                if not parent.exists():
                    print(parent)
                    raise Exception("Invalid sponsor selected")
                else:
                    parent = parent[0]
                if CoreTestMpttNode.objects.filter(marketing_plan=core_plan, user=info.context.user, parent=parent).exists():
                    raise Exception("Layer already exists")
        # create it at this point
        payment_type = PaymentType.objects.filter(type_id=payment_type)
        if not payment_type.exists:
            raise Exception("payment type not found")
        _ord = CoreMlmOrders.objects.create(
            billing_info=binfo, product=core_plan,
            ordered_by=info.context.user, sponsor=CustomUser.objects.get(
                user_id=sponsor
            ), payment_type=payment_type[0])
        # if this marketing plan is getting registered for the first time then consider it as the first ancestor of the whole network

        return CreateCoreMlmOrder(payload=True)


class CreateGenv2(graphene.Mutation):
    payload = graphene.Field(CoreTestMpttType)

    class Arguments:
        parent = graphene.String()
        marketing_plan = graphene.String()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, parent, marketing_plan):
        if not CoreLevelPlans.objects.get(core_id=marketing_plan).exists():
            raise Exception("Marketing plan not found")
        if not CustomUser.objects.get(user_id=parent).exists():
            raise Exception("Parent not found")
        try:
            # add to the user package to his list
            # create an layer object
            parent = CoreTestMpttNode.objects.get(user=CustomUser.objects.get(
                user_id=parent
            ))

            obj = CoreTestMpttNode.objects.create(parent=parent, user=info.context.user, marketing_plan=CoreLevelPlans.objects.get(
                core_id=marketing_plan
            ))
        except Exception as e:
            raise Exception("Error adding layer [{}]".format(str(e)))
        return CreateGenv2(payload=obj)


class CreateTestLayer(graphene.Mutation):
    payload = graphene.String()
    # create a new layer and form a valid ogg tree

    class Arguments:
        affilate = graphene.String()
        plan = graphene.String()

    def mutate(self, info, affilate, plan):
        try:
            plan = CoreLevelPlans.objects.get(core_id=plan)
            aff = Affilate.objects.get(affilate_id=affilate)
            # find the parent of the affilate that brought this user
            tstParent = TestNetwork.objects.filter(
                user=aff.user, marketing_plan=plan)
            print("DEBUG")
            print(tstParent)
            print("DEBUG")
            # first find the parent for this relation
            if tstParent.exists():
                # layer if there is an ancestory relation
                layer = TestNetwork.objects.create(
                    parent=tstParent[0], marketing_plan=plan, affilate=aff, user=info.context.user)
            else:
                # Set None parent to the first user in the net work
                layer = TestNetwork.objects.create(
                    parent=None, marketing_plan=plan, affilate=aff, user=info.context.user)
        except Exception as e:
            raise Exception(str(e))
        return CreateTestLayer(payload=str(layer.layer_id))


class CreateMlmLayer(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        marketing_plan = graphene.String()
        user = graphene.types.UUID()

    @permissions_checker([AffilatePermission, IsAuthenticated])
    def mutate(self, info, marketing_plan, user):
        # TODO implement layers add
        # user -> uid
        usr = CustomUser.objects.get(user_id=user)
        _nnet = UnilevelNetwork.objects.create(
            # user=usr, affilate=Affilate.objects.get(
            #     affilate_i
            # )
        )
        return CreateMlmLayer(payload=True)


# this is where the plan order is granted and orders approved
class AddPlanMutation(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        plan_type = graphene.String()
        core_id = graphene.String()
        ven_id = graphene.String()

    @permissions_checker([AffilatePermission])
    def mutate(self, info, plan_type, core_id, ven_id):
        valid_types = ["core", "ven"]
        if not plan_type in valid_types:
            raise Exception("Plan Type not found")
        if plan_type == "core":
            if not UUID_PATTERN.match(core_id):
                # not valid uuid pattern
                raise Exception("value unkonwn")
            qs = CoreLevelPlans.objects.filter(core_id=core_id)
            if not qs.exists():
                raise Exception("core plan not found")
        else:
            if not UUID_PATTERN.match(ven_id):
                # not valid uuid pattern
                raise Exception("value unkonwn")
            qs = VendorLevelPlans.objects.filter(core_id=ven_id)
            if not qs.exists():
                raise Exception("vend plan not found")

        if plan_type == "core":
            print(qs[0], "!"*200)
            AffilatePlans.objects.create(
                core_plan=qs[0],
                plan_type="core",
                affilate=Affilate.objects.get(
                    user=info.context.user
                )
            )
        else:
            AffilatePlans.objects.create(
                vendor_plan=qs[0],
                plan_type="ven",
                affilate=Affilate.objects.get(
                    user=info.context.user
                )
            )

        # except Exception as e:
        #     raise str(e)

        return AddPlanMutation(payload=True)
