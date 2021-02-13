import re
import graphene
from .types import AffilatePlansType
from vendors.models import VendorLevelPlans, Vendor
from vendors.types import VendorPlanType, VendorType
from accounts.models import Affilate, CoreLevelPlans
from django_graphene_permissions import permissions_checker
from .models import AffilatePlans, UnilevelNetwork
from ashewa_final.core_perimssions import AffilatePermission
from django_graphene_permissions.permissions import IsAuthenticated
from accounts.models import CustomUser

from core_marketing.models import TestNetwork, CoreTestMpttNode, CoreLevelPlans, CoreMlmOrders, CoreVendorMlmOrders, BillingInfo
from core_marketing.types import CoreTestMpttType, CoreMlmOrderType, CoreVendorMlmOrderType
UUID_PATTERN = re.compile(
    r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


class CreateCoreMlmOrder(graphene.Mutation):
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
        try:
            core_plan = CoreLevelPlans.objects.get(
                core_id=mlm)
            if(sponsor == str(info.context.user.user_id)):
                raise Exception("User can't be a sponsor")
            # get sponsor and add to the layer
            _ord = CoreMlmOrders.objects.create(
                billing_info=binfo, product=core_plan,
                ordered_by=info.context.user,sponsor=CustomUser.objects.get(
                    user_id=sponsor
                ))
            sponsor_user = CustomUser.objects.get(user_id=sponsor)
            # if this marketing plan is getting registered for the first time then consider it as the first ancestor of the whole network
            if CoreTestMpttNode.objects.filter(marketing_plan=core_plan, user=info.context.user, parent=CoreTestMpttNode.objects.get(
                user=sponsor_user
            )).exists():
                raise Exception("Layer already exists")

            if not CoreTestMpttNode.objects.filter(marketing_plan=core_plan).exists():
                # first ancestors don't have any parent
                mlmNode = CoreTestMpttNode.objects.create(
                    user=info.context.user, parent=None, marketing_plan=core_plan)
            else:
                # old code pop this off later
                # if CoreTestMpttNode.objects.filter(user=info.context.user)
                mlmNode = CoreTestMpttNode.objects.create(
                    user=info.context.user, parent=CoreTestMpttNode.objects.get(
                        user=sponsor_user
                    ),
                    # setup marketing plan in the nodes
                    marketing_plan=core_plan
                )
            mlmNode.initiate_nodes_logic()
        except Exception as e:
            raise Exception("ERROR: Order {}".format(str(e)))

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
