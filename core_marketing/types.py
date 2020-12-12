import graphene
from accounts.models import Affilate
from graphene_django import DjangoObjectType
from accounts.types import AffilateType, CoreUsersType
from .models import CoreLevelPlans, UnilevelNetwork, AffilatePlans


class CoreMarketingPlanTypes(DjangoObjectType):
    class Meta:
        model = CoreLevelPlans


class DoubleNet(graphene.ObjectType):
    user = graphene.List(CoreUsersType)
    level = graphene.Int()


class SingleNet(graphene.ObjectType):
    user = graphene.List(CoreUsersType)
    level = graphene.Int()
    children = graphene.List(lambda: DoubleNet)


class SingleNetworkLayerType(graphene.ObjectType):
    user = graphene.List(CoreUsersType)
    core_level = graphene.Int()
    children = graphene.List(SingleNet)


class AffilatePlansType(DjangoObjectType):
    class Meta:
        model = AffilatePlans


class CorePlanPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(CoreMarketingPlanTypes)
    total = graphene.Int()
