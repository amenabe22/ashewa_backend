import re
import graphene
from .models import AffilatePlans
from .types import AffilatePlansType
from vendors.models import VendorLevelPlans, Vendor
from vendors.types import VendorPlanType, VendorType
from accounts.models import Affilate, CoreLevelPlans
from django_graphene_permissions import permissions_checker
from ashewa_final.core_perimssions import AffilatePermission


UUID_PATTERN = re.compile(
    r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


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
            print(qs[0],"!"*200)
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