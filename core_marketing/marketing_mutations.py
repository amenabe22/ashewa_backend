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
from core_marketing.models import TestNetwork
UUID_PATTERN = re.compile(
    r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


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
