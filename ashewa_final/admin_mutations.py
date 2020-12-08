import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from .core_perimssions import AdminPermission
from core_marketing.models import CoreLevelPlans
from accounts.models import Admin


class CreateMarketingPlans(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        plan_name = graphene.String()
        plan_desc = graphene.String()
        joining_fee = graphene.String()

    @permissions_checker([AdminPermission])
    def mutate(self, info, plan_name, plan_desc, joining_fee):
        CoreLevelPlans.objects.create(
            creator=Admin.objects.get(user=info.context.user),
            plan_name=plan_name, plan_description=plan_desc
        )
        return CreateMarketingPlans(success=True)

