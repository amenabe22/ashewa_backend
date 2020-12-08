import graphene
from graphene_django import DjangoObjectType
from .models import CoreLevelPlans, UnilevelNetwork
from accounts.types import AffilateType, CoreUsersType
from accounts.models import Affilate


class CoreMarketingPlanTypes(DjangoObjectType):
    class Meta:
        model = CoreLevelPlans

class SingleNetworkLayerType(graphene.ObjectType):
    user = graphene.List(CoreUsersType)
    level = graphene.Int()
